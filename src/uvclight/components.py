# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de

import zope.lifecycleevent

from cromlech.browser import ITemplate
from cromlech.browser.exceptions import HTTPFound
from cromlech.browser.exceptions import HTTPRedirect
from cromlech.browser.exceptions import REDIRECTIONS
from cromlech.browser.interfaces import ITypedRequest
from cromlech.browser.utils import redirect_exception_response
from cromlech.webob.response import Response
from dolmen.forms import crud
from dolmen.forms.base import Form, Fields
from dolmen.forms.base import action
from dolmen.forms.base.interfaces import IForm
from dolmen.forms.ztk.validation import InvariantsValidation
from dolmen.layout import Layout
from dolmen.location import get_absolute_url
from dolmen.menu import IMenu, Menu as BaseMenu, Entry as MenuItem
from dolmen.message import BASE_MESSAGE_TYPE
from dolmen.message.utils import send
from dolmen.request.decorators import request_type
from dolmen.template import TALTemplate
from dolmen.view import View as BaseView, make_layout_response
from dolmen.viewlet import ViewletManager, Viewlet

from grokcore.component import Adapter, MultiAdapter, GlobalUtility
from grokcore.component import adapter, implementer, baseclass, name
from grokcore.security import Permission

from z3c.table.column import Column, GetAttrColumn, LinkColumn
from z3c.table.table import Table
from zope.component import getMultiAdapter, getAdapters
from zope.event import notify
from zope.interface import Interface

from .directives import implements
from .directives import layer
from .directives import viewletmanager
from .directives import title 
from dolmen.menu import menuentry
from .interfaces import ISubMenu, IContextualActionsMenu
from .utils import get_template, make_json_response, url as compute_url


class Layout(Layout):
    baseclass()
    responseFactory = Response


class View(BaseView):
    baseclass()
    responseFactory = Response

    def url(self, obj, name=None, data=None):
        return compute_url(self.request, obj, name, data)

    def application_url(self):
        return self.request.application_url

    def flash(self, message, type=BASE_MESSAGE_TYPE):
        return send(message, type=type)

    
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
    FORM_MACROS = get_template('formmacro.cpt')

    template = None

    def url(self, obj, name=None, data=None):
        return compute_url(self.request, obj, name, data)

    def application_url(self):
        return self.request.application_url

    def flash(self, message, type=BASE_MESSAGE_TYPE):
        return send(message, type=type)

    def namespace(self):
        namespace = super(Form, self).namespace()
        namespace['macro'] = self.FORM_MACROS.macros
        return namespace

    def redirect(self, url, code=302):
        exception = REDIRECTIONS[code]
        raise exception(url)
    
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


class ContextualActionsMenu(Menu):
    implements(IContextualActionsMenu)
    name('contextualactionsmenu')
    baseclass()


class AddForm(Form):
    title(u'Erstellen')
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


#@menuentry(IContextualActionsMenu)
class EditForm(crud.Edit, Form):
    title(u'Bearbeiten')
    baseclass()


#@menuentry(ContextualActionsMenu)
class DisplayForm(crud.Display, Form):
    title(u'Anzeigen')
    baseclass()


#@menuentry(ContextualActionsMenu)
class DefaultView(DisplayForm):
    name('index')
    title(u'Anzeigen')
    baseclass()
    responseFactory = Response
    make_response = make_layout_response


#@menuentry(ContextualActionsMenu)
class DeleteForm(crud.Delete, Form):
    title(u'Entfernen')


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


class LinkColumn(LinkColumn):
    baseclass()

    def getLinkURL(self, item):
        """Setup link url."""
        if self.linkName is not None:
            return '%s/%s' % (get_absolute_url(item, self.request), self.linkName)
        return get_absolute_url(item, self.request)


@request_type('rest')
class IRESTRequest(ITypedRequest):
    """REST/JSON request"""


class MethodNotAllowed(Exception):
    """Exception indicating that an attempted REST method is not allowed."""


class REST(View):
    layer(IRESTRequest)
    baseclass()

    def __call__(self):
        try:
            method = getattr(self, self.request.method)
            result = method()
            return self.make_response(result)
        except HTTPRedirect, exc:
            return redirect_exception_response(self.responseFactory, exc)

    def GET(self):
        raise MethodNotAllowed(self.context, self.request)

    def POST(self):
        raise MethodNotAllowed(self.context, self.request)

    def PUT(self):
        raise MethodNotAllowed(self.context, self.request)

    def DELETE(self):
        raise MethodNotAllowed(self.context, self.request)


