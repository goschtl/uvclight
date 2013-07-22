# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de

from uvclight.components import View, Layout, Page, Form, Fields
from uvclight.components import ViewletManager, Viewlet
from uvclight.utils import get_template
from dolmen.forms.base import action
from dolmen.menu import Menu

from uvclight.directives import (
    order,
    context,
    implementer,
    implements,
    layer,
    name,
    viewletmanager,
    )
