# -*- coding: utf-8 -*-
# Copyright (c) 2007-2013 NovaReto GmbH
# cklinger@novareto.de

try:
    from .components import Page
    from .directives import context, name
    from .utils import get_template
    from .events import UserLoggedInEvent
    
    from barrel import form
    from cromlech.browser import IPublicationRoot
    from cromlech.browser import exceptions
    from cromlech.browser import getSession, IResponseFactory, ILayout
    from cromlech.security import Interaction, unauthenticated_principal
    from cromlech.security import Principal
    from cromlech.webob import Request
    from dolmen.view import query_view
    from grokcore.security import permissions
    from webob.exc import HTTPTemporaryRedirect
    from zope.component import queryMultiAdapter, getUtility
    from zope.event import notify
    from zope.interface import implementer
    from zope.location import Location
    from zope.security import canAccess
    from zope.security.checker import CheckerPublic
    from zope.security.management import getInteraction
    from zope.security.proxy import removeSecurityProxy
    from zope.security.simplepolicies import ParanoidSecurityPolicy
    from zope.securitypolicy.interfaces import IRole
    from zope.security.proxy import removeSecurityProxy

    unauthenticated_principal.roles = set()
    unauthenticated_principal.permissions = set()


    class Principal(Principal):

        def __init__(self, id, **attrs):
            self.id = id
            self.title = attrs.get('title', u'')
            self.description = attrs.get('description', u'')
            self.roles = attrs.get('roles', set())
            self.permissions = attrs.get('permissions', set())


    def get_layout(authform, request):
        return queryMultiAdapter((request, authform), ILayout, name="")


    @implementer(IPublicationRoot, IResponseFactory)
    class Auth(Location, form.FormAuth):
        """
        """
        session_user_key = "user"

        def __init__(self, users, realm):
            self.users = users
            self.realm = realm

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


    def do_logout(global_conf, session_key):
        def logout(environ, start_response):
            session = environ[session_key].session
            if session is not None:
                if 'user' in session:
                    del session['user']
            response = HTTPTemporaryRedirect(location='/')
            return response(environ, start_response)
        return logout


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


    def getPermissionForRole(role):
        role = getUtility(IRole, role)
        return set(permissions.bind().get(role))


    class SimpleSecurityPolicy(ParanoidSecurityPolicy):
        public = frozenset(('zope.View', CheckerPublic))

        @staticmethod
        def get_permissions(principal):
            permissions = principal.permissions
            for role in principal.roles:
                permissions |= getPermissionForRole(role)
            return permissions

        def checkPermission(self, permission, object):
            if permission in self.public:
                return True
            
            for participation in self.participations:
                permissions = self.get_permissions(participation.principal)
                print permissions
                if permission in permissions:
                    return True
            return False


    def security_check(lookup):
        def check(*args, **kwargs):
            component = lookup(*args, **kwargs)
            if component is not None:
                if canAccess(component, '__call__'):
                    return removeSecurityProxy(component)
                else:
                    interaction = getInteraction()
                    principal = interaction.participations[0].principal
                    if principal is unauthenticated_principal:
                        raise exceptions.HTTPUnauthorized(component)
                    else:
                        raise exceptions.HTTPForbidden(component)
            return None
        return check

except ImportError:
    #print "The Auth Module was not Loaded"
    raise
