# -*- coding: utf-8 -*-

from .components import Form, Fields, action
from .directives import name, context, require
from .events import UserLoggedInEvent

from cromlech.browser import exceptions, getSession
from dolmen.forms.base import FAILURE, SuccessMarker
from zope.component import getUtility
from zope.component.hooks import getSite
from zope.event import notify
from zope.interface import Interface
from zope.schema import TextLine, Password


try:
    from . import auth

    def make_principal(*args):
        return auth.Principal(*args)
        
except ImportError:

    def make_principal(*args):
        raise NotImplementedError


class ICredentials(Interface):

    def assert_credentials(username, password):
        """Returns a boolean
        """


class ILoginForm(Interface):

    username = TextLine(
        title=u'Username',
        required=True)

    password = Password(
        title=u"Password",
        required=True)


class Login(Form):
    name('login')
    context(Interface)
    require('zope.Public')

    fields = Fields(ILoginForm)
    
    @action(u'Login')
    def log_me(self):
        data, errors = self.extractData()
        if errors:
            self.submissionError = errors
            return FAILURE

        # credentials here
        site = getSite()
        if site is None:
            self.flash(u"You can't login here.")
            return SuccessMarker(
                'Login failed', False, url=self.url(self.context), code=302)

        credentials = getattr(site, 'credentials', None)
        if not credentials:
            self.flash(u"Missing credentials.")
            return SuccessMarker(
                'Login failed', False, url=self.url(self.context), code=302)

        for credential in credentials:
            credentials_manager = getUtility(ICredentials, name=credential)
            account = credentials_manager.log_in(**data)
            if account:
                session = getSession()
                session['username'] = data['username']
                self.flash(u"Login successful.")
                principal = make_principal(data['username'])
                self.request.principal = principal
                notify(UserLoggedInEvent(principal))
                return SuccessMarker(
                    'Login successful', True, url=self.url(self.context),
                    code=302)

        self.flash(u'Login failed.')
        return FAILURE
