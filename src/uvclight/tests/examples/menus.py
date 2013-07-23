# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de


import uvclight
from zope.interface import Interface


class GlobalMenu(uvclight.Menu):
    __name__ = u"globalmenu"
    __parent__ = None
    uvclight.context(Interface)


class AddMenu(uvclight.SubMenu):
    uvclight.menu(GlobalMenu)

    def render(self):
        return u"BLA"


class Entry(uvclight.MenuItem):
    uvclight.menu(AddMenu)
