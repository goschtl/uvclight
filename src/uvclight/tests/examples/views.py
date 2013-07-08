# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de


import uvclight

from grokcore.component import Context
from zope.interface import Interface



class MyView(uvclight.View):
    uvclight.context(Context)
    uvclight.name('index')

    def update(self):
        self.name = u"Christian"

    def render(self):
        return u"Hello World %s" % (self.name)


class MyLayout(uvclight.Layout):
    uvclight.context(Interface)
    template = uvclight.get_template('layout.cpt', __file__)


class Page(uvclight.Page):
    uvclight.context(Context)

    def update(self):
        self.name = u"Christian"

    def render(self):
        return u"Hello World %s" % (self.name)
