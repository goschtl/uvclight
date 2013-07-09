# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de

from dolmen.view import View, make_layout_response
from cromlech.webob.response import Response
from dolmen.layout import Layout
from dolmen.viewlet import ViewletManager, Viewlet
from dolmen.forms.ztk import Form


class View(View):
    responseFactory = Response


class Layout(Layout):
    responseFactory = Response


class Page(View):
    responseFactory = Response
    make_response = make_layout_response


class Form(Form):
    responseFactory = Response
    make_response = make_layout_response
