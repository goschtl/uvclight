# -*- coding: utf-8 -*-
# Copyright (c) 2007-2013 NovaReto GmbH
# cklinger@novareto.de

try:
    from .components import View, Page
    from .directives import context, name
    from .utils import get_template
    from .interfaces import UserLoggedInEvent

    from barrel import form
    from cromlech.browser import IPublicationRoot
    from cromlech.browser import getSession, IView, IResponseFactory, ILayout
    from cromlech.security import Interaction
    from cromlech.security import Principal
    from cromlech.webob import Request, Response
    from dolmen.view import query_view
    from zope.component import queryMultiAdapter
    from zope.event import notify
    from zope.interface import Interface, implementer
    from zope.location import Location
    from zope.security import canAccess
    from zope.security.proxy import removeSecurityProxy
    from zope.security.simplepolicies import ParanoidSecurityPolicy


    class Principal(Principal):

        def __init__(self, id, title=u'', description=u'', roles=[],
                     permissions=[]):
            self.id = id
            self.title = title
            self.description = description
            self.roles = roles
            self.permissions = permissions


    def get_layout(authform, request):
        return queryMultiAdapter((request, authform), ILayout, name="")


    def logout(session=None):
        if session is None:
            session = getSession()
        if 'REMOTE_USER' in session:
            del session['REMOTE_USER']
            return True
        return False


    @implementer(IPublicationRoot, IView, IResponseFactory)
    class Auth(Location, form.FormAuth):
        """
        """
        session_user_key = "user"
        __component_name__ = '/login'
        
        def __init__(self, users, realm):
            self.users = users
            self.realm = realm

        @property
        def context(self):
            return self
            
        def valid_user(self, username, password):
            """Is this a valid username/password? (True or False)"""
            account = self.users.get(username, None)
            if account is not None and account.password == password:
                notify(UserLoggedInEvent(Principal(username)))
                return True
            return False

        def session_dict(self, environ):
            ses = getSession()
            return ses

        def save_session(self):
            pass

        def not_authenticated(self, environ, start_response):
            """Respond to an unauthenticated request with a form.
            """
            request = Request(environ)
            view = query_view(request, self, name='login')
            if view is None:
                raise NotImplementedError
        
            with Interaction():
                response = view()
            return response(environ, start_response)

        def __call__(self, app):
            """If request is not from an authenticated user, complain."""
            def security_traverser(environ, start_response):
                if self.authenticate(environ):
                    return app(environ, start_response)
                return self.not_authenticated(environ, start_response)
            return security_traverser


    class Login(Page):
        context(Auth)
        name('login')
        template = get_template('login.cpt')

        title = message = u"Please log in"
        action = ""
        
        def update(self):
            self.username = self.request.environment.get(
                self.context.environ_user_key, '')

            self.userfield = self.context.user_field
            self.pwdfield = self.context.pass_field
            self.button = self.context.button


    def secured(users, realm):
        """Decorator to secure my apps with.
        """
        def deco(app):
            auth = Auth(users, realm)
            return auth(app)
        return deco


    class SimpleSecurityPolicy(ParanoidSecurityPolicy):

        def checkPermission(self, permission, object):
            if permission == 'zope.View':
                return True
            principals = [p.principal for p in self.participations]
            for principal in principals:
                permissions = getattr(principal, 'permissions', set())
                if permission in permissions:
                    return True
            return False

    def security_check(lookup):
        def check(*args, **kwargs):
            component = lookup(*args, **kwargs)
            if component is not None:
                assert canAccess(component, '__call__')   # or raise
                return removeSecurityProxy(component)
            return None
        return check

except ImportError:
    print "The Auth Module was not Loaded"
