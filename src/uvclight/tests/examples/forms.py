# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de


import uvclight

from zope.interface import Interface
from zope.schema import TextLine, Choice


class IPerson(Interface):

    name = TextLine(
        title=u"Name",
        description=u"Please enter a valid name.",
    )

    gender = Choice(
        title=u"Gender",
        description=u"Please choose your gender.",
        values=('men', 'women'),
    )


class MyForm(uvclight.Form):
    uvclight.context(Interface)
    fields = uvclight.Fields(IPerson)

    @uvclight.action('Save')
    def handle_save(self):
        data, errors = self.extractData()
        return
