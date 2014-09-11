# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de

import uvclight
from uvclight import interfaces
from zope.interface import Interface


@uvclight.implementer(interfaces.IHeaders)
class Headers(uvclight.ViewletManager):
    uvclight.name('uvc-headers')
    uvclight.context(Interface)


@uvclight.implementer(interfaces.IPageTop)
class PageTop(uvclight.ViewletManager):
    uvclight.name('uvc-pagetop')
    uvclight.context(Interface)


@uvclight.implementer(interfaces.IAboveContent)
class AboveContent(uvclight.ViewletManager):
    uvclight.name('uvc-above-body')
    uvclight.context(Interface)


@uvclight.implementer(interfaces.IBelowContent)
class BelowContent(uvclight.ViewletManager):
    uvclight.name('uvc-below-body')
    uvclight.context(Interface)


@uvclight.implementer(interfaces.IFooter)
class Footer(uvclight.ViewletManager):
    uvclight.name('uvc-footer')
    uvclight.context(Interface)


@uvclight.implementer(interfaces.IExtraInfo)
class ExtraInfo(uvclight.ViewletManager):
    uvclight.name('uvc-extrainfo')
    uvclight.context(Interface)
