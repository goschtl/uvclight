# -*- coding: utf-8 -*-
# Copyright (c) 2007-2013 NovaReto GmbH
# cklinger@novareto.de

from zope.interface import Interface, implementer
from cromlech.browser import IView
from uvc.design.canvas import *


class IXMLRPCView(IView):
    pass


class IUserLoggedInEvent(Interface):
    """ """


@implementer(IUserLoggedInEvent)
class UserLoggedInEvent(object):

    def __init__(self, principal):
        self.principal = principal

