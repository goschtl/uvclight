# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de

from dolmen.view import View, make_layout_response
from cromlech.webob.response import Response
from dolmen.layout import Layout
from dolmen.viewlet import ViewletManager, Viewlet
from dolmen.forms.base import Form, Fields, action
from dolmen.forms.ztk.validation import InvariantsValidation
from dolmen.menu import Menu, Entry as MenuItem
from zope.component import getMultiAdapter
from cromlech.browser import ITemplate
from grokcore.component import adapter, implementer
from zope.interface import Interface
from dolmen.forms.base.interfaces import IForm
from grokcore.component import baseclass
from uvclight.utils import get_template


class View(View):
    baseclass()
    responseFactory = Response


class Layout(Layout):
    baseclass()
    responseFactory = Response


class Page(View):
    baseclass()
    responseFactory = Response
    make_response = make_layout_response


class Menu(Menu):
    baseclass()
    css = "nav"


class Form(Form):
    baseclass()
    responseFactory = Response
    make_response = make_layout_response
    dataValidators = [InvariantsValidation]

    template = None

    def render(self):
        """Template is taken from the template attribute or searching
        for an adapter to ITemplate for entry and request
        """
        template = getattr(self, 'template', None)
        if template is None:
            template = getMultiAdapter((self, self.request), ITemplate)
        return template.render(
            self, target_language=self.target_language, **self.namespace())


@adapter(IForm, Interface)
@implementer(ITemplate)
def menu_template(context, request):
    """default template for the menu"""
    return get_template('form.cpt', __file__)
