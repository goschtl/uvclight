# -*- coding: utf-8 -*-
# Copyright (c) 2007-2013 NovaReto GmbH
# cklinger@novareto.de

import traceback

from .components import View, Page
from .utils import get_template

from dawnlight import ResolveError
from grokcore.component import name, context
from grokcore.security import require
from cromlech.dawnlight import ITracebackAware
from zope.dublincore.interfaces import IDCDescriptiveProperties
from zope.location import locate, Location
from zope.interface import implementer


@implementer(IDCDescriptiveProperties)
class Error404(Location):

    def __init__(self, context):
        self.context = context
        locate(self, context.__parent__, context.__name__)

    @property
    def title(self):
        return u"Not found"

    @property
    def description(self):
        return str(self.context)


@implementer(ITracebackAware)
class PageError404(Page):
    name('')
    context(ResolveError)
    require('zope.Public')

    template = get_template('404.cpt')

    def __init__(self, context, request):
        self.context = Error404(context)
        self.request = request

    def set_exc_info(self, exc_info):
        self.traceback = ''.join(traceback.format_exception(*exc_info))


@implementer(IDCDescriptiveProperties)
class Error500(Location):

    def __init__(self, context):
        self.context = context
        locate(self, context.__parent__, context.__name__)

    @property
    def title(self):
        return u"Server error"

    @property
    def description(self):
        return str(self.context)


@implementer(ITracebackAware)
class PageError500(Page):
    name('')
    context(Exception)
    require('zope.Public')

    template = get_template('500.cpt')

    def __init__(self, context, request):
        self.context = Error500(context)
        self.request = request

    def set_exc_info(self, exc_info):
        self.traceback = ''.join(traceback.format_exception(*exc_info))
