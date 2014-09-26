# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de

from unidecode import unidecode

from cromlech.browser import ITemplate
from cromlech.browser.exceptions import HTTPFound
from cromlech.browser.exceptions import HTTPRedirect
from cromlech.browser.exceptions import REDIRECTIONS
from cromlech.browser.interfaces import ITypedRequest
from cromlech.browser.utils import redirect_exception_response
from cromlech.container.components import Container as BaseContainer
from cromlech.container.contained import Contained
from cromlech.container.interfaces import IContainer, INameChooser
from cromlech.webob.response import Response

from dolmen.forms import crud
from dolmen.forms.base import Form as BaseForm, Fields
from dolmen.forms.base import action
from dolmen.forms.base.markers import HiddenMarker
from dolmen.forms.base.interfaces import IForm, IModeMarker
from dolmen.forms.table import TableForm as BaseTableForm
from dolmen.forms.ztk.validation import InvariantsValidation
from dolmen.forms.composed import ComposedForm, SubForm

from dolmen.layout import Layout as BaseLayout
from dolmen.location import get_absolute_url
from dolmen.menu import menu
from dolmen.menu import IMenu, Menu as BaseMenu, Entry as MenuItem
from dolmen.message import BASE_MESSAGE_TYPE
from dolmen.message.utils import send
from dolmen.request.decorators import request_type
from dolmen.template import TALTemplate
from dolmen.view import View as BaseView, make_layout_response
from dolmen.viewlet import ViewletManager, Viewlet
from dolmen.forms.viewlet import ViewletForm, ViewletManagerForm

from grokcore.component import Adapter, MultiAdapter, GlobalUtility
from grokcore.component import adapter, implementer, baseclass, name
from grokcore.component import global_utility
from grokcore.security import Permission

from z3c.table.column import Column, GetAttrColumn, LinkColumn
from z3c.table.column import ModifiedColumn, CheckBoxColumn
from z3c.table.table import Table as BaseTable

import zope.lifecycleevent
from zope.component import getMultiAdapter, getAdapters
from zope.event import notify
from zope.interface import Interface, implements
from zope.dublincore.interfaces import IDCDescriptiveProperties

from uvc.content import schematic_bootstrap

from .directives import implements, context, schema
from .directives import layer, title, order
from .directives import viewletmanager
from .interfaces import ISubMenu, IContextualActionsMenu
from .interfaces import IContent, IDescriptiveSchema
from .utils import make_xmlrpc_response, make_json_response
from .utils import get_template, url as compute_url


class Content(Contained):
    """Base Content
    """
    schema(IDescriptiveSchema)
    implements(IContent)
    __init__ = schematic_bootstrap


class Container(BaseContainer):
    """Base Container
    """
    implements(IContent, IContainer)
    schema(IDescriptiveSchema)
    __init__ = schematic_bootstrap


class Layout(BaseLayout):
    baseclass()
    context(Interface)
    responseFactory = Response


class View(BaseView):
    baseclass()
    context(Interface)
    responseFactory = Response

    def url(self, obj, name=None, data=None):
        """This function does something.

        Args:
            obj (object):  The ILocation providing object.

        Kwargs:
            name (str): .
            data (dict): .

        Returns:
            str.

        """
        return compute_url(self.request, obj, name, data)

    def application_url(self):
        return self.request.application_url

    def flash(self, message, type=BASE_MESSAGE_TYPE):
        return send(message, type=type)

    def redirect(self, url, code=302):
        exception = REDIRECTIONS[code]
        raise exception(url)


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
    context(Interface)
    viewletmanager(IMenu)

    def __init__(self, context, request, view, parentmenu=None):
        Menu.__init__(self, context, request, view)
        self.parentmenu = parentmenu

    def update(self):
        BaseMenu.update(self)


class Form(BaseForm):
    baseclass()
    context(Interface)
    responseFactory = Response
    make_response = make_layout_response
    dataValidators = [InvariantsValidation]

    template = None
    widgets_css = {}

    def url(self, obj, name=None, data=None):
        return compute_url(self.request, obj, name, data)

    def application_url(self):
        return self.request.application_url

    def flash(self, message, type=BASE_MESSAGE_TYPE):
        return send(message, type=type)

    def namespace(self):
        namespace = super(Form, self).namespace()
        namespace['macro'] = self.getTemplate().macros
        return namespace

    def redirect(self, url, code=302):
        exception = REDIRECTIONS[code]
        raise exception(url)

    def isHidden(self, widget):
        mode = widget.component.mode
        return IModeMarker.providedBy(mode) and isinstance(HiddenMarker, mode)

    def getTemplate(self):
        template = getMultiAdapter((self, self.request), ITemplate)
        return template

    def updateWidgets(self):
        super(Form, self).updateWidgets()
        for field, styles in self.widgets_css.items():
            uid = '%s.%s.%s' % (self.prefix, field.prefix, field.identifier)
            self.fieldWidgets[uid].htmlClass = lambda: styles

    def render(self):
        """Template is taken from the template attribute or searching
        for an adapter to ITemplate for entry and request
        """
        template = getattr(self, 'template', None)
        if template is None:
            template = getMultiAdapter((self, self.request), ITemplate)
        return template.render(
            self, target_language=self.target_language, **self.namespace())


class ViewletForm(ViewletForm):
    baseclass()

    def namespace(self):
        namespace = super(ViewletForm, self).namespace()
        namespace['macro'] = self.getTemplate().macros
        return namespace

    def getTemplate(self):
        template = getMultiAdapter((self, self.request), ITemplate)
        return template


@adapter(IForm, Interface)
@implementer(ITemplate)
def form_template(context, request):
    """default template for the menu"""
    return get_template('form.cpt', __file__)


class AddForm(Form):
    title(u'Erstellen')
    #baseclass()
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
    title(u'Bearbeiten')
    baseclass()
    
    
class EditMenuItem(MenuItem):
    menu(IContextualActionsMenu)
    title(u'Bearbeiten')
    name('edit')
    order(20)


class DisplayForm(crud.Display, Form):
    title(u'Anzeigen')
    baseclass()
    

class DefaultView(DisplayForm):
    name('index')
    title(u'Anzeigen')
    baseclass()
    responseFactory = Response
    make_response = make_layout_response


class DisplayMenuItem(MenuItem):
    menu(IContextualActionsMenu)
    title(u'Anzeigen')
    name('index')
    order(10)


class DeleteForm(crud.Delete, Form):
    title(u'Entfernen')
    baseclass()


class DeleteMenuItem(MenuItem):
    menu(IContextualActionsMenu)
    title('Entfernen')
    name('delete')
    order(30)


class Table(BaseTable):

    def getBatchSize(self):
        return int(self.request.form.get(
            self.prefix + '-batchSize', self.batchSize))

    def getBatchStart(self):
        return int(self.request.form.get(
            self.prefix + '-batchStart', self.batchStart))

    def getSortOn(self):
        """Returns sort on column id.
        """
        return self.request.form.get(self.prefix + '-sortOn', self.sortOn)

    def getSortOrder(self):
        """Returns sort order criteria.
        """
        return self.request.form.get(
            self.prefix + '-sortOrder', self.sortOrder)


class TableView(Table, View):
    baseclass()
    context(Interface)

    def update(self):
        Table.update(self)


class TablePage(Table, Page):
    baseclass()
    context(Interface)

    def update(self):
        Table.update(self)

    def render(self):
        if self.template:
            return self.template.render(
                self, target_language=self.target_language, **self.namespace())
        return self.renderTable()


class LinkColumn(LinkColumn):
    baseclass()

    def getLinkURL(self, item):
        """Setup link url."""
        if self.linkName is not None:
            return '%s/%s' % (
                get_absolute_url(item, self.request), self.linkName)
        return get_absolute_url(item, self.request)


class CheckBoxColumn(CheckBoxColumn):
    baseclass()

    def isSelected(self, item):
        v = self.request.form.get(self.getItemKey(item), [])
        if not isinstance(v, list):
            # ensure that we have a list which prevents to compare strings
            v = [v]
        if self.getItemValue(item) in v:
            return True
        return False


class ModifiedColumn(ModifiedColumn):
    baseclass()


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


class TableForm(BaseTableForm):
    baseclass()
    context(Interface)

    responseFactory = Response
    make_response = make_layout_response


class NormalizingNamechooser(Adapter):
    implements(INameChooser)
    context(IContainer)

    retries = 100

    def __init__(self, context):
        self.context = context

    def checkName(self, name, object):
        return not name in self.context

    def _findUniqueName(self, name, object):
        if not name in self.context:
            return name

        idx = 1
        while idx <= self.retries:
            new_name = "%s_%d" % (name, idx)
            if not new_name in self.context:
                return new_name
            idx += 1

        raise ValueError(
            "Cannot find a unique name based on "
            "`%s` after %d attempts." % (name, self.retries))

    def chooseName(self, name, object):
        if not name:
            dc = IDCDescriptiveProperties(object, None)
            if dc is not None and dc.title:
                name = dc.title.strip()
                name = unidecode(name).strip().replace(' ', '_').lower()
            else:
                name = object.__class__.__name__.lower()

        return self._findUniqueName(name, object)
