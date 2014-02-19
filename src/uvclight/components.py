# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de

from cromlech.browser import ITemplate
from cromlech.webob.response import Response
from dolmen.forms.base import Form, Fields
from dolmen.forms.base.interfaces import IForm
from dolmen.forms.ztk.validation import InvariantsValidation
from dolmen.layout import Layout
from dolmen.menu import IMenu, Menu as BaseMenu, Entry as MenuItem
from dolmen.view import View as BaseView, make_layout_response
from grokcore.component import adapter, implementer, baseclass
from dolmen.viewlet import ViewletManager, Viewlet
from zope.component import getMultiAdapter, getAdapters
from zope.interface import Interface

from .directives import viewletmanager
from .utils import get_template, make_json_response
from .interfaces import ISubMenu
from z3c.table.table import Table
from z3c.table.column import Column


class Layout(Layout):
    baseclass()
    responseFactory = Response


class View(BaseView):
    baseclass()
    responseFactory = Response


class Page(View):
    baseclass()
    make_response = make_layout_response


class JSON(View):
    baseclass()
    make_response = make_json_response


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


class TableView(Table, View):
    baseclass()

    def update(self):
        Table.update(self)


class TablePage(Table, Page):
    baseclass()

    def update(self):
        Table.update(self)
