# -*- coding: utf-8 -*-
# Copyright (c) 2007-2013 NovaReto GmbH
# cklinger@novareto.de

import uvclight
from zope.interface import Interface


class RESTView(uvclight.REST):
    uvclight.context(Interface)

    def GET(self):
        return "GET"

    def PUT(self):
        return "PUT"

    def POST(self):
        return "POST"

    def DELETE(self):
        return "DELETE"


class RestViewNoPut(uvclight.REST):
    uvclight.context(Interface)

    def GET(self):
        return "GET"
