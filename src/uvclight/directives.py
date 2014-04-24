# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de

from cromlech.browser.directives import request as layer, view
from dolmen.viewlet import slot as viewletmanager
from grokcore.component import baseclass, context, name
from grokcore.component import order, title, implements, provides
from grokcore.security import require
from zope.interface import implements, implementer
from dolmen.menu import menu

try:
    from dolmen.content import schema
except ImportError:
    print "`schema` directive is available only with the zodb extra. This is a `dolmen.content` limitation."
    def schema(*args, **kwargs):
        raise NotImplementedError
