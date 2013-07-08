# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de

from cromlech.browser.testing import TestRequest
from grokcore.component import Context
from zope.component import getMultiAdapter

class TestViewComponents:
    request = TestRequest()
    context = Context()

    def test_base_view(self, config):
        view = getMultiAdapter((self.context, self.request), name='index')
        assert view is not None
        view.update()
        html = view.render()
        assert html == "Hello World Christian"


    def test_base_page(self, config):
        page = getMultiAdapter((self.context, self.request), name='page')
        assert page is not None
        page.update()
        html = page()
        assert html == "<body>Hello World Christian</body>"

