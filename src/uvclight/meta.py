# -*- coding: utf-8 -*-

import martian
from dolmen.menu import IMenu
from zope.interface import Interface
from zope.component import provideAdapter
from .interfaces import ISubMenu
from .components import SubMenu
from . import directives


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
