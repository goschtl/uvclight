# -*- coding: utf-8 -*-


from .context import ContextualRequest
from .publishing import located_view, secured_view, base_model_lookup
from .session import sessionned


from .security import Interaction
from cromlech.browser import getSession
from cromlech.dawnlight import DawnlightPublisher
from cromlech.security import unauthenticated_principal
from zope.security.proxy import removeSecurityProxy
from uvclight.utils import with_zcml, with_i18n


try:
    from .auth import Principal
except:
    class Principal(object):
        def __init__(self, user):
            self.user = user


class Publication(object):

    layers = None

    #@classmethod
    #def create(cls, session_key='session.key'):
    #    return cls(session_key)

    @classmethod
    @with_zcml('zcml_file')
    @with_i18n('langs', fallback='en')
    def create(cls, gc, name, session_key):
        return cls(name, session_key)

    def __init__(self, name, session_key):
        self.publish = self.get_publisher()
        self.name = name
        self.session_key = session_key

    def get_publisher(
            self, view_lookup=located_view, model_lookup=base_model_lookup):
        publisher = DawnlightPublisher(model_lookup, view_lookup)
        return publisher.publish

    def get_credentials(self, environ):
        pass

    def principal_factory(self, username):
        pass

    def site_manager(self, environ):
        raise NotImplementedError

    def publish_traverse(self, request, site):
        return self.publish(request, site)

    def __call__(self, environ, start_response):

        @sessionned(self.session_key)
        def publish(environ, start_response):
            layers = self.layers or list()
            with ContextualRequest(environ, layers=layers) as request:
                site_manager = self.site_manager(environ)
                with site_manager as site:
                    response = self.publish_traverse(request, site)
                    return response(environ, start_response)

        return publish(environ, start_response)



class SecurePublication(Publication):

    layers = None

    def get_publisher(
            self, view_lookup=secured_view, model_lookup=base_model_lookup):
        publisher = DawnlightPublisher(model_lookup, view_lookup)
        return publisher.publish

    def get_credentials(self, environ):
        session = getSession()
        user = environ.get('REMOTE_USER') or session.get('username')

    def principal_factory(self, username):
        if username:
            return Principal(user)
        return unauthenticated_principal

    def publish_traverse(self, request, site):
        user = self.get_credentials(request.environment)
        request.principal = self.principal_factory(user)
        with Interaction(request.principal):
            response = self.publish(request, site)
            response = removeSecurityProxy(response)
            return response
