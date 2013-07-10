# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de

from cromlech.browser.testing import TestRequest, TestView
from grokcore.component import Context
from zope.component import getMultiAdapter
from dolmen.viewlet.interfaces import IViewSlot


class TestViewComponents:
    request = TestRequest()
    context = Context()

    def test_base_view(self, config):
        view = getMultiAdapter((self.context, self.request), name='index')
        assert view is not None
        view.update()
        html = view.render()
        assert html == "Hello World Christian"
        assert view().body == "Hello World Christian"

    def test_base_page(self, config):
        page = getMultiAdapter((self.context, self.request), name='page')
        assert page is not None
        page.update()
        html = str(page().body)
        assert html == "<body>Hello World Christian</body>\n"


class TestViewletComponents:
    request = TestRequest()
    context = Context()
    view = TestView(context, request)

    def test_get_ViewletManager(self, config):
        vlm = getMultiAdapter((self.context, self.request, self.view),
                              IViewSlot, name=u"header")
        assert vlm is not None
        vlm.update()
        assert len(vlm.viewlets) == 1
        viewlet = vlm.viewlets[0]
        assert viewlet.render() == "Hello World"


class TestFormComponents:
    request = TestRequest()
    context = Context()

    def test_base_form(self, config):
        form = getMultiAdapter((self.context, self.request), name=u"myform")
        form.update()
        fields = [x.identifier for x in form.fields]
        assert 'gender' in fields
        assert 'name' in fields
        actions = [x.identifier for x in form.actions]
        assert 'save' in actions
        assert form().status == '200 OK'
