# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de

from cromlech.browser.testing import TestRequest, TestView
from grokcore.component import Context
from zope.component import getMultiAdapter
from dolmen.viewlet.interfaces import IViewSlot
from zope.location.interfaces import ILocation
from zope.interface import alsoProvides
from cromlech.browser import IPublicationRoot
from dolmen.viewlet.interfaces import IViewletManager
from z3c.table.interfaces import IColumn


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


class TestJSONComponents:
    request = TestRequest()
    context = Context()

    def test_base_view(self, config, app):
        view = getMultiAdapter((self.context, self.request), name='myjsonview')
        assert view is not None
        view.update()
        view.render()
        json = view()
        assert json.body == '{"name": "Christian"}'
        from json import loads
        pd = loads(json.body)
        assert 'name' in pd.keys()
        from infrae.testbrowser import Browser
        browser = Browser(app)
        browser.handleErrors = False
        browser.open('http://locahost/myjsonview')
        assert browser.contents == '{"name": "Christian"}'
        browser.open('http://locahost/myjsonview' )


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
    context.__name__ = "contact"
    context.__parent__ = None

    def test_base_form(self, config):
        alsoProvides(self.context, ILocation)
        alsoProvides(self.context, IPublicationRoot)
        form = getMultiAdapter((self.context, self.request), name=u"myform")
        form.update()
        fields = [x.identifier for x in form.fields]
        assert 'gender' in fields
        assert 'name' in fields
        actions = [x.identifier for x in form.actions]
        assert 'save' in actions
        assert form().status == '200 OK'


class TestMenuComponents:
    request = TestRequest()
    context = Context()
    context.__name__ = "contact"
    context.__parent__ = None
    view = TestView(context, request)

    def test_get_ViewletManager(self, config):
        alsoProvides(self.context, ILocation)
        alsoProvides(self.context, IPublicationRoot)
        globalmenu = getMultiAdapter((self.context, self.request, self.view),
                                     IViewletManager, name=u"globalmenu")
        globalmenu.update()
        assert len(globalmenu.submenus) == 1
        assert globalmenu.submenus[0].viewlets[0].title == "entry"


class TestTableComponent:
    request = TestRequest()
    context = Context()

    def test_tableView(self, config):
        table = getMultiAdapter((self.context, self.request), name="tableview")
        table.update()
        assert 1 == len(table.columns)
        column = getMultiAdapter(
            (self.context, self.request, table),
            IColumn,
            name="idcolumn"
        )
        assert column.id == "id_id"
        assert column.header == "ID Column"

    def test_tablePage(self, config):
        table = getMultiAdapter((self.context, self.request), name="tablepage")
        table.update()
        assert 1 == len(table.columns)
