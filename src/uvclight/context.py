# -*- coding: utf-8 -*-

from .http import setRequest
from cromlech import webob


class Request(object):

    def __init__(self, environ, factory=webob.Request):
        self.environ = environ
        self.factory = factory

    def __enter__(self):
        request = self.factory(self.environ)
        setRequest(request)
        return request

    def __exit__(self, type, value, traceback):
        setRequest()
