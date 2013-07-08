# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de


import uvclight
from zope.interface import Interface


class Header(uvclight.ViewletManager):
    uvclight.context(Interface)


class GlobalMenu(uvclight.Viewlet):
    uvclight.context(Interface)
    uvclight.viewletmanager(Header)

    def render(self):
        return u"Hello World"
