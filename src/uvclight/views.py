# -*- coding: utf-8 -*-
# Copyright (c) 2007-2013 NovaReto GmbH
# cklinger@novareto.de

from dawnlight import ResolveError
from .components import View
from .utils import get_template
from grokcore.component import name, context, implements
from grokcore.security import require
from zope.dublincore.interfaces import IDCDescriptiveProperties
from zope.location import locate, LocationProxy


class Error404(LocationProxy):
    implements(IDCDescriptiveProperties)

    def __init__(self, context):
        self.context = context
        locate(self, context.__parent__, context.__name__)

    @property
    def title(self):
        return u"Not found"

    @property
    def description(self):
        return str(self.context)


class PageError404(View):
    name('')
    context(ResolveError)
    require('zope.Public')

    template = get_template('404.cpt')

    def __init__(self, context, request):
        self.context = Error404(context)
        self.request = request
        self.message = context.message


class Error500(LocationProxy):
    implements(IDCDescriptiveProperties)

    def __init__(self, context):
        self.context = context
        locate(self, context.__parent__, context.__name__)

    @property
    def title(self):
        return u"There is an Error"

    @property
    def description(self):
        return str(self.context)


class PageError500(View):
    name('')
    context(Exception)
    require('zope.Public')

    template = get_template('500.cpt')

    def __init__(self, context, request):
        self.context = Error500(context)
        self.request = request
        self.message = context.message
