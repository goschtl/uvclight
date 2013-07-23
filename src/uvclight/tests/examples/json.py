# -*- coding: utf-8 -*-
# Copyright (c) 2007-2013 NovaReto GmbH
# cklinger@novareto.de

import uvclight
from zope.interface import Interface


class MyJsonView(uvclight.JSON):
    uvclight.context(Interface)

    def render(self):
        return dict(name=u"Christian")
