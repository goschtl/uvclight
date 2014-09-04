# -*- coding: utf-8 -*-

from .components import Page
from .directives import name, context, require
from cromlech.browser import exceptions
from dolmen.forms.base import FAILURE, SuccessMarker


class UnauthorizedPage(Page):
    name('')
    context(exceptions.HTTPUnauthorized)
    require('zope.Public')

    def render(self):
        obj = self.context.__parent__
        self.flash(
            u"This page is protected and you're not allowed."
            u" Please login.")
        self.redirect(self.url(obj) + '/login')

    
class ForbiddenPage(Page):
    name('')
    context(exceptions.HTTPForbidden)
    require('zope.Public')

    def render(self):
        return u"This page is protected and you don't have the credentials."
