# -*- coding: utf-8 -*-

from zope.event import notify
from grokcore.component import subscribe
from zope.interface import implementer, Interface
from zope.component.interfaces import ObjectEvent, IObjectEvent
from cromlech.browser import PublicationBeginsEvent, PublicationEndsEvent
from cromlech.browser import IPublicationBeginsEvent, IPublicationEndsEvent


class IApplicationInitializedEvent(IObjectEvent):
    pass


@implementer(IApplicationInitializedEvent)
class ApplicationInitializedEvent(ObjectEvent):
    pass


class IUserLoggedInEvent(Interface):
    """Event triggered when a user logged in.
    """


@implementer(IUserLoggedInEvent)
class UserLoggedInEvent(object):

    def __init__(self, principal):
        self.principal = principal
