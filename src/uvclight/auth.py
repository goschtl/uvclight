# -*- coding: utf-8 -*-
# Copyright (c) 2007-2013 NovaReto GmbH
# cklinger@novareto.de

try:
    import string
    from barrel import form
    from cromlech.browser import getSession
    from cromlech.webob import Request, Response
    from zope.event import notify
    from uvclight.interfaces import UserLoggedInEvent
    from cromlech.security import Principal
    from zope.security.simplepolicies import ParanoidSecurityPolicy
    from zope.security import canAccess
    from zope.security.proxy import removeSecurityProxy


    class Principal(Principal):

        def __init__(self, id, title=u'', description=u'', roles=[], permissions=[]):
            self.id = id
            self.title = title
            self.description = description
            self.roles = roles
            self.permissions = permissions


    class MyLayout(object):
        def render(self, result, **namespace):
            return "<html> %s </html>" % result


    LAYOUT = MyLayout()


    def render_in_layout(result, responseFactory=Response, **namespace):
        wrapped = LAYOUT.render(result, **namespace)
        response = responseFactory()
        response.write(wrapped or u'')
        return response


    default_template = """
        <h1>Resource Requires Authentication</h1>
        <form method="POST" action="">
            <fieldset>
                <legend>$message:</legend>
                <label for="$user_field">Username:</label>
                <input type="text"
                    name="$user_field"
                    id="$user_field"
                    value="$username"/>
                <br/>
                <label for="$pass_field">Password:</label>
                <input type="password" name="$pass_field" id="$pass_field"/>
                <br/>
                <button type="submit"
                        name="$button"
                        id="$button"
                        value="submit">Sign In</button>
            </fieldset>
        </form>
    """


    def logout(session=None):
        if session is None:
            session = getSession()
        if 'REMOTE_USER' in session:
            del session['REMOTE_USER']
            return True
        return False


    class Auth(form.FormAuth):
        """
        """
        session_user_key = "user"
        template = string.Template(default_template)

        def __init__(self, users, realm):
            self.users = users
            self.realm = realm

        def valid_user(self, username, password):
            """Is this a valid username/password? (True or False)"""
            pwd = self.users.get(username, None)
            if pwd:
                if pwd == password:
                    notify(UserLoggedInEvent(Principal(username)))
                    return True
            return False

        def session_dict(self, environ):
            ses = getSession()
            return ses

        def save_session(self):
            pass

        def not_authenticated(self, environ, start_response):
            """Respond to an unauthenticated request with a form."""
            username = environ.get(self.environ_user_key, '')
            if username:
                message = self.failed_message
            else:
                message = self.first_message

            html = self.template.safe_substitute(
                user_field=self.user_field,
                pass_field=self.pass_field,
                button=self.button,
                username=username,
                message=message,
                **environ)

            request = Request(environ)
            namespace = {'context': self,
                         'request': request,
                         'view': self,
                         'content': html}
            layout = render_in_layout(html, **namespace)
            return layout(environ, start_response)

        def __call__(self, app):
            """If request is not from an authenticated user, complain."""
            def security_traverser(environ, start_response):
                if self.authenticate(environ):
                    return app(environ, start_response)
                return self.not_authenticated(environ, start_response)
            return security_traverser

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
                if permission in principal.permissions:
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
