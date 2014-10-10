# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de

from unidecode import unidecode

from .directives import implements, context, schema
from cromlech.browser.interfaces import ITypedRequest
from cromlech.browser.utils import redirect_exception_response
from cromlech.container.interfaces import IContainer, INameChooser
from dolmen.forms import crud
from dolmen.forms.base import Form as BaseForm, Fields
from dolmen.forms.base import action
from dolmen.forms.base.interfaces import IForm, IModeMarker
from dolmen.forms.base.markers import HiddenMarker
from dolmen.forms.composed import ComposedForm, SubForm
from dolmen.forms.table import TableForm as BaseTableForm
from dolmen.forms.ztk.validation import InvariantsValidation
from grokcore.component import Adapter, MultiAdapter, GlobalUtility
from grokcore.component import adapter, implementer, baseclass, name
from grokcore.component import global_utility
from grokcore.security import Permission
from uvc.content import schematic_bootstrap
from z3c.table.column import Column, GetAttrColumn, LinkColumn
from z3c.table.column import ModifiedColumn, CheckBoxColumn

from uvc.content.components import *
from uvc.browser.components import *


@request_type('rest')
class IRESTRequest(ITypedRequest):
    """REST/JSON request"""


class MethodNotAllowed(Exception):
    """Exception indicating that an attempted REST method is not allowed.
    """


class REST(View):
    layer(IRESTRequest)
    baseclass()

    def __call__(self):
        try:
            method = getattr(self, self.request.method)
            result = method()
            return self.make_response(result)
        except HTTPRedirect, exc:
            return redirect_exception_response(self.responseFactory, exc)

    def GET(self):
        raise MethodNotAllowed(self.context, self.request)

    def POST(self):
        raise MethodNotAllowed(self.context, self.request)

    def PUT(self):
        raise MethodNotAllowed(self.context, self.request)

    def DELETE(self):
        raise MethodNotAllowed(self.context, self.request)


class NormalizingNamechooser(Adapter):
    implements(INameChooser)
    context(IContainer)

    retries = 100

    def __init__(self, context):
        self.context = context

    def checkName(self, name, object):
        return not name in self.context

    def _findUniqueName(self, name, object):
        if not name in self.context:
            return name

        idx = 1
        while idx <= self.retries:
            new_name = "%s_%d" % (name, idx)
            if not new_name in self.context:
                return new_name
            idx += 1

        raise ValueError(
            "Cannot find a unique name based on "
            "`%s` after %d attempts." % (name, self.retries))

    def chooseName(self, name, object):
        if not name:
            dc = IDCDescriptiveProperties(object, None)
            if dc is not None and dc.title:
                name = dc.title.strip()
                name = unidecode(name).strip().replace(' ', '_').lower()
            else:
                name = object.__class__.__name__.lower()

        return self._findUniqueName(name, object)
