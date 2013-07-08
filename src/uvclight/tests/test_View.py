# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de

from cromlech.browser.testing import TestRequest
from grokcore.component import Context
from zope.component import getMultiAdapter

class TestView:

    def test_base_view(self, config):
        request = TestRequest()
        context = Context()
        view = getMultiAdapter((context, request), name='myview')
        view.update()
        html = view.render()
        assert view is not None
        assert html == "Hello World Christian"
