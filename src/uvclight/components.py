# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de

from .directives import implements, context
from cromlech.browser.directives import request as layer
from cromlech.browser.exceptions import HTTPRedirect
from cromlech.browser.interfaces import ITypedRequest
from cromlech.browser.utils import redirect_exception_response
from cromlech.container.interfaces import IContainer
from dolmen.request.decorators import request_type
from grokcore.component import Adapter
from grokcore.component import baseclass
from ul.browser.components import View


@request_type('rest')
class IRESTRequest(ITypedRequest):
    """REST/JSON request"""


class MethodNotAllowed(Exception):
    """Exception indicating that an attempted REST method is not allowed.
    """


class REST(View):
    layer(IRESTRequest)
    baseclass()

    def __call__(self):
        try:
            method = getattr(self, self.request.method)
            result = method()
            return self.make_response(result)
        except HTTPRedirect, exc:
            return redirect_exception_response(self.responseFactory, exc)

    def GET(self):
        raise MethodNotAllowed(self.context, self.request)

    def POST(self):
        raise MethodNotAllowed(self.context, self.request)

    def PUT(self):
        raise MethodNotAllowed(self.context, self.request)

    def DELETE(self):
        raise MethodNotAllowed(self.context, self.request)


CHUNK = 1 << 18


def make_pdf(self, result):
    response = self.responseFactory()
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = (
        u'attachment; filename="%s.csv"' % self.view.__class__.__name__
    )

    def filebody(r):
        data = r.read(CHUNK)
        while data:
            yield data
            data = r.read(CHUNK)

    response.app_iter = filebody(result)
    return response


class PDF(View):
    baseclass()
    make_response = make_pdf

    def render(self):
        raise NotImplementedError('Return your own file-like object')
