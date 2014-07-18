# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de

from cromlech.browser import setSession, getSession
from cromlech.browser import IPublicationRoot as IRootObject
from dolmen.forms.base import SuccessMarker, SUCCESS, FAILURE
from dolmen.forms.base import action, Action, Fields, Actions
from dolmen.forms.base.interfaces import ISuccessMarker
from dolmen.forms.base.markers import Marker
from dolmen.view import query_view
from dolmen.menu import menuentry
from zope.component.hooks import getSite


from .session import (
    sessionned,
    )

from .utils import (
    get_template,
    current_principal,
    url,
    )

from .interfaces import (
    IContextualActionsMenu,
    IContent,
    IDescriptiveSchema,
    )

from .components import (
    Adapter,
    AddForm,
    Column,
    Content,
    DefaultView,
    DeleteForm,
    DisplayForm,
    EditForm,
    Fields,
    Form,
    ComposedForm,
    SubForm,
    Form as Wizard, # FIXME
    Form as Step, # FIXME
    GetAttrColumn,
    GlobalUtility,
    Index,
    JSON,
    Layout,
    LinkColumn,
    Menu,
    MenuItem,
    MultiAdapter,
    Page,
    Permission,
    REST,
    SubMenu,
    TablePage,
    TableView,
    TableForm,
    View,
    Viewlet,
    ViewletManager,
    )

from uvclight.directives import (
    adapts,
    baseclass,
    context,
    description,
    implementer,
    implements,
    layer,
    menu,
    name,
    form,
    order,
    provides,
    require,
    schema,
    title,
    traversable,
    view,
    viewletmanager,
    schema,
    )

from .security import (
    IUnauthenticatedPrincipal,
    Interaction,
    Participation,
    Principal,
    unauthenticated_principal,
    )
