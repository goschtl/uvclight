# -*- coding: utf-8 -*-
# Copyright (c) 2007-2013 NovaReto GmbH
# cklinger@novareto.de

from zope.interface import Interface, implementer

from cromlech.browser import IView
from dolmen.menu.interfaces import IMenu
from dolmen.viewlet.interfaces import IViewSlot


class IXMLRPCView(IView):
    pass


#
### User Logged In Event
#


class IUserLoggedInEvent(Interface):
    """ """


@implementer(IUserLoggedInEvent)
class UserLoggedInEvent(object):

    def __init__(self, principal):
        self.principal = principal


#
### Viewlet Managers
#


class IPageTop(IViewSlot):
    """Marker For the area that sits at the top of the page.
    """


class ITabs(IViewSlot):
    """Marker for the action tabs.
    """


class IAboveContent(IViewSlot):
    """Marker For the area that sits above the page body.
    """


class IBelowContent(IViewSlot):
    """Marker For the area that sits under the page body.
    """


class IHeaders(IViewSlot):
    """Marker For Headers
    """


class IToolbar(IViewSlot):
    """Marker for Toolbar
    """


class IFooter(IViewSlot):
    """ """


class IExtraInfo(IViewSlot):
    """ """


#
### Menus
#


class IGlobalMenu(IMenu):
    """Marker for GlobalMenu
    """


class IPersonalPreferences(IMenu):
    """Marker for PersonalPreferences
    """


class IFooterMenu(IMenu):
    """Marker for Footer
    """


class IDocumentActions(IMenu):
    """Marker for DocumentActions
    """


class IExtraViews(IMenu):
    """Marker for additional Views for Folders
       Objects etc...
    """


class IPersonalMenu(IMenu):
    """Marker for PersonalMenu
    """


class IContextualActionsMenu(IMenu):
    """Marker for PersonalMenu
    """

#
### SubMENU
#


class ISubMenu(IMenu):
    pass
