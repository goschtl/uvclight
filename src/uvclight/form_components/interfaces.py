# -*- coding: utf-8 -*-

from zope.interface import Interface
from zope.schema.interfaces import IASCIILine


class ICaptcha(IASCIILine):
    """A field for captcha validation
    """


class IOptionalChoice(Interface):
    pass
