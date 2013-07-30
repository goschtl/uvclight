# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de

import json

from os import path
from cromlech.browser import ITemplate
from cromlech.webob.response import Response
from dolmen.forms.base import Form, Fields, action
from dolmen.forms.base.interfaces import IForm
from dolmen.forms.ztk.validation import InvariantsValidation
from dolmen.layout import Layout
from dolmen.menu import IMenu, Menu as BaseMenu, Entry as MenuItem
from dolmen.view import View, make_layout_response
from dolmen.viewlet import ViewletManager, Viewlet
from grokcore.component import adapter, implementer
from grokcore.component import baseclass
from uvclight.utils import get_template
from uvclight.interfaces import ISubMenu
from zope.component import getMultiAdapter, getAdapters
from zope.interface import Interface
from .directives import viewletmanager


class View(View):
    baseclass()
    responseFactory = Response


def make_json_response(view, result, name=None):
    return json.dumps(result)


class JSON(View):
    baseclass()
    responseFactory = Response

    def make_response(self, struct):
        json_result = json.dumps(struct)
        response = self.responseFactory()
        response.write(json_result)
        response.headers['Content-Type'] = 'application/json'
        return response


class Layout(Layout):
    baseclass()
    responseFactory = Response


class Page(View):
    baseclass()
    responseFactory = Response
    make_response = make_layout_response


class Menu(BaseMenu):
    baseclass()
    css = "nav"

    submenus = None
    #template = get_template("menu_with_submenus.pt")

    def update(self):
        self.submenus = list()
        BaseMenu.update(self)
        submenus = getAdapters(
            (self.context, self.request, self.view, self), ISubMenu)
        for name, submenu in submenus:
            submenu.update()
            self.submenus.append(submenu)


class SubMenu(Menu):
    baseclass()
    viewletmanager(IMenu)

    def __init__(self, context, request, view, parentmenu=None):
        Menu.__init__(self, context, request, view)
        self.parentmenu = parentmenu

    def update(self):
        BaseMenu.update(self)


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
