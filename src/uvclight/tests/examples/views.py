# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de


import uvclight
from grokcore.component import Context
from zope.interface import Interface


class MyView(uvclight.View):
    uvclight.context(Context)

    def update(self):
        self.name = u"Christian"

    def render(self):
        return u"Hello World %s" % (self.name)

