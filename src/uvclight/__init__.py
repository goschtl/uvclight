# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de


from .components import ViewletManager, Viewlet
from .utils import get_template

from dolmen.forms.base import SUCCESS, FAILURE, action, Action, Fields, Actions
from dolmen.forms.base.interfaces import ISuccessMarker
from dolmen.forms.base.markers import Marker
from dolmen.view import query_view


from uvclight.components import (
    View,
    Layout,
    Page,
    Form,
    Fields,
    Menu,
    SubMenu,
    MenuItem,
    JSON,
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
    )
