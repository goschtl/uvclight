# -*- coding: utf-8 -*-
# Copyright (c) 2007-2013 NovaReto GmbH
# cklinger@novareto.de

from zope.interface import Interface, implementer
from cromlech.browser import IView
from uvc.design.canvas import *
from uvc.content import IContent, IDescriptiveSchema
from cromlech.browser import IPublicationRoot


class IXMLRPCView(IView):
    pass


class IApplication(IPublicationRoot):
    pass
