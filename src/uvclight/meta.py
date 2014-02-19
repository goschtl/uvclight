# -*- coding: utf-8 -*-

import martian
from zope.interface import Interface
from zope.component import provideAdapter
from .interfaces import ISubMenu
from .components import SubMenu, Column
from . import directives
from z3c.table.interfaces import ITable, IColumn
from dolmen.view.meta import default_view_name


class SubMenuGrokker(martian.ClassGrokker):
    martian.component(SubMenu)
    martian.directive(directives.context, default=Interface)
    martian.directive(directives.layer, default=Interface)
    martian.directive(directives.view, default=Interface)
    martian.directive(directives.viewletmanager, default=None)

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
    martian.directive(directives.context, default=Interface)
    martian.directive(directives.layer, default=Interface)
    martian.directive(directives.view, default=ITable)
    martian.directive(directives.provides, default=IColumn)
    martian.directive(directives.name, get_default=default_view_name)

    def execute(self, factory, config, context, request, view, provides, name):
        for_ = (context, request, view)
        config.action(
            discriminator=('adapter', for_, provides, name),
            callable=provideAdapter,
            args=(factory, for_, provides, name),
        )
        return True
