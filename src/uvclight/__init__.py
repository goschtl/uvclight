# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de

from .components import ViewletManager, Viewlet
from .utils import get_template, current_principal

from cromlech.browser import IPublicationRoot as IRootObject
from dolmen.forms.base import SUCCESS, FAILURE, action, Action, Fields, Actions
from dolmen.forms.base.interfaces import ISuccessMarker
from dolmen.forms.base.markers import Marker
from dolmen.view import query_view
from dolmen.menu import menuentry
from zope.component.hooks import getSite


from uvclight.interfaces import (
    IContextualActionsMenu,
    )


from uvclight.components import (
    View,
    Layout,
    Page,
    Index,
    Form,
    AddForm,
    EditForm,
    DisplayForm,
    DeleteForm,
    DefaultView,
    Fields,
    Menu,
    SubMenu,
    MenuItem,
    JSON,
    TableView,
    TablePage,
    Column,
    REST,
    )

from uvclight.directives import (
    order,
    context,
    implementer,
    implements,
    layer,
    name,
    require,
    title,
    view,
    viewletmanager,
    menu,
    schema,
    )
