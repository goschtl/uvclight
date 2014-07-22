# -*- coding: utf-8 -*-

from zope.interface import implementer, Interface
from zope.interface.interfaces import ObjectEvent


class IApplicationInitializedEvent(Interface):
    pass


@implementer(IApplicationInitializedEvent)
class ApplicationInitializedEvent(ObjectEvent):
    pass
