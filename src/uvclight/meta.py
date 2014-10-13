# -*- coding: utf-8 -*-

import martian
from cromlech.browser import request as layer
from dolmen.view.meta import default_view_name
from dolmen.viewlet import context, view, slot as viewletmanager
from grokcore.component import name, provides
from ul.browser.components import SubMenu
from uvc.design.canvas import ISubMenu
from z3c.table.column import Column
from z3c.table.interfaces import ITable, IColumn
from zope.component import provideAdapter
from zope.interface import Interface


class SubMenuGrokker(martian.ClassGrokker):
    martian.component(SubMenu)
    martian.directive(context, default=Interface)
    martian.directive(layer, default=Interface)
    martian.directive(view, default=Interface)
    martian.directive(viewletmanager, default=None)

    def execute(self,
                factory, config, context, request, view, slot):
        if slot is not None:
            config.action(
                discriminator=('SubMenu', context, request, view, slot),
                callable=provideAdapter,
                args=(factory, (context, request, view, slot), ISubMenu, u''))
            return True
        return False


class ColumnGrokker(martian.ClassGrokker):
    martian.component(Column)
    martian.directive(context, default=Interface)
    martian.directive(layer, default=Interface)
    martian.directive(view, default=ITable)
    martian.directive(provides, default=IColumn)
    martian.directive(name, get_default=default_view_name)

    def execute(self, factory, config, context, request, view, provides, name):
        for_ = (context, request, view)
        config.action(
            discriminator=('adapter', for_, provides, name),
            callable=provideAdapter,
            args=(factory, for_, provides, name),
        )
        return True
