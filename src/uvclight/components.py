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
from grokcore.component import adapter, implementer, baseclass, name
from dolmen.viewlet import ViewletManager, Viewlet
from zope.component import getMultiAdapter, getAdapters
from zope.interface import Interface

from .directives import viewletmanager
from .utils import get_template, make_json_response
from .interfaces import ISubMenu
from z3c.table.table import Table
from z3c.table.column import Column
from dolmen.forms import crud
from dolmen.forms.base import action
from zope.event import notify
import zope.lifecycleevent
from cromlech.browser.exceptions import HTTPFound


class Layout(Layout):
    baseclass()
    responseFactory = Response


class View(BaseView):
    baseclass()
    responseFactory = Response

    def application_url(self):
        return self.request.application_url

    
class Page(View):
    baseclass()
    make_response = make_layout_response


class Index(Page):
    baseclass()
    name('index')
    make_response = make_layout_response
    

class JSON(View):
    baseclass()
    make_response = make_json_response


class Menu(BaseMenu):
    baseclass()
    css = "nav"

    submenus = None

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

    def application_url(self):
        return self.request.application_url
    
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



class AddForm(Form):
    baseclass()
    _finishedAdd = False

    @action(u'Speichern', identifier="uvcsite.add")
    def handleAdd(self):
        data, errors = self.extractData()
        if errors:
            self.flash('Es sind Fehler aufgetreten')
            return
        obj = self.createAndAdd(data)
        if obj is not None:
            # mark only as finished if we get the new object
            self._finishedAdd = True

    def createAndAdd(self, data):
        obj = self.create(data)
        notify(zope.lifecycleevent.ObjectCreatedEvent(obj))
        self.add(obj)
        return obj

    def create(self, data):
        raise NotImplementedError

    def add(self, object):
        raise NotImplementedError

    def nextURL(self):
        raise NotImplementedError

    def render(self):
        if self._finishedAdd:
            raise HTTPFound(self.nextURL())
            self.request.response.redirect(self.nextURL())
            return ""
        return super(AddForm, self).render()


class EditForm(crud.Edit, Form):
    baseclass()


class DisplayForm(crud.Display, Form):
    baseclass()


class DefaultView(DisplayForm):
    name('index')
    baseclass()
    responseFactory = Response
    make_response = make_layout_response
    

class DeleteForm(crud.Delete, Form):
    pass


class Table(Table):

    def getBatchSize(self):
        return int(self.request.form.get(self.prefix + '-batchSize',
            self.batchSize))

    def getBatchStart(self):
        return int(self.request.form.get(self.prefix + '-batchStart',
            self.batchStart))

    def getSortOn(self):
        """Returns sort on column id."""
        return self.request.form.get(self.prefix + '-sortOn', self.sortOn)

    def getSortOrder(self):
        """Returns sort order criteria."""
        return self.request.form.get(self.prefix + '-sortOrder',
            self.sortOrder)


class TableView(Table, View):
    baseclass()

    def update(self):
        Table.update(self)


class TablePage(Table, Page):
    baseclass()

    def update(self):
        Table.update(self)
