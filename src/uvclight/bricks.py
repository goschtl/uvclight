# -*- coding: utf-8 -*-

from .auth import Principal
from .context import ContextualRequest
from .publishing import create_base_publisher
from .security import Interaction
from .session import sessionned

from cromlech.browser import getSession
from cromlech.security import unauthenticated_principal
from zope.security.proxy import removeSecurityProxy


class SecurePublication(object):

    def __init__(self, session_key, layers=None):
        self.layers = layers or list()
        self.publish = self.get_publisher()
        self.session_key = session_key

    def get_publisher(self):
        return create_base_publisher(secure=True).publish
        
    def get_credentials(self, environ):
        session = getSession()
        user = environ.get('REMOTE_USER') or session.get('username')

    def principal_factory(self, username):
        if username:
            return Principal(user)
        return unauthenticated_principal

    def site_manager(self):
        raise NotImplementedError
    
    def __call__(self, environ, start_response):

        @sessionned(self.session_key)
        def publish(environ, start_response):
            with ContextualRequest(environ, layers=self.layers) as request:
                user = self.get_credentials(environ)
                request.principal = self.principal_factory(user)
                site_manager = self.site_manager(environ)

                with site_manager as site:
                    with Interaction(request.principal):
                        response = self.publish(request, site)
                        response = removeSecurityProxy(response)
                        return response(environ, start_response)

        return publish(environ, start_response)
