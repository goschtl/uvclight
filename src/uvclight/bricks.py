# -*- coding: utf-8 -*-

from .auth import Principal
from .context import ContextualRequest
from .publisher import create_base_publisher
from .security import Interaction
from .session import sessionned

from cromlech.security import unauthenticated_principal
from cromlech.zodb import Site, get_site


class SecurePublication(object):

    layers = frozenset([IDGUVRequest])
    
    def __init__(self, environ_key, name, session_key):
        self.name = name
        self.environ_key = environ_key
        self.session_key = session_key
        self.publish = self.get_publisher().publish

    def get_publisher(self):
        return create_base_publisher(secure=True)
        
    def get_credentials(self, environ):
        session = getSession()
        user = environ.get('REMOTE_USER') or session.get('username')

    def principal_factory(self, username):
        if username:
            return Principal(user)
        return unauthenticated_principal
    
    def __call__(self, environ, start_response):

        @sessionned(self.session_key)
        def publish(environ, start_response):
            with ContextualRequest(environ, layers=self.layers) as request:
                user = self.get_credentials(environ)
                request.principal = self.principal_factory(user)
                sm = self.site_manager(environ)

                with site:
                    with Interaction(request.principal):
                        response = self.publish(request, site)
                        response = removeSecurityProxy(response)
                        return response(environ, start_response)

        return publish(environ, start_response)
