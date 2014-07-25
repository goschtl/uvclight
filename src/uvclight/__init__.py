# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de

from cromlech.browser import IPublicationRoot as IRootObject
from cromlech.browser import setSession, getSession
from dolmen.forms.base import SuccessMarker, SUCCESS, FAILURE
from dolmen.forms.base import action, Action, Fields, Actions
from dolmen.forms.base.interfaces import ISuccessMarker
from dolmen.forms.base.markers import Marker
from dolmen.menu import menuentry
from dolmen.view import query_view
from zope.component.hooks import getSite
from zope.event import notify
from zope.interface import implementer
from zope.location import Location

# We don't want to directly expose the contextual managers.
# their names would conflict. They are to be used through the
# 'context' import.
from . import context


from .session import (
    sessionned,
    )

from .http import (
    setRequest,
    getRequest,
    )

from .utils import (
    get_template,
    current_principal,
    url,
    load_zcml,
    )

from .events import (
    ApplicationInitializedEvent,
    IApplicationInitializedEvent,
    IObjectEvent,
    IPublicationBeginsEvent,
    IPublicationEndsEvent,
    IUserLoggedInEvent,
    ObjectEvent,
    PublicationBeginsEvent,
    PublicationEndsEvent,
    UserLoggedInEvent,
    )

from .interfaces import (
    IApplication,
    IContextualActionsMenu,
    IContent,
    IDescriptiveSchema,
    )

from .publishing import (
    DawnlightPublisher,
    ViewLookup,
    view_locator,
    create_base_publisher,
    )

from .components import (
    Adapter,
    AddForm,
    Column,
    Content,
    Container,
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
    CheckBoxColumn,
    ModifiedColumn,
    GlobalUtility,
    global_utility,
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
    adapter,
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
