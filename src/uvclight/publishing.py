# -*- coding: utf-8 -*-

from cromlech.dawnlight import ViewLookup
from cromlech.dawnlight import view_locator, query_view
from cromlech.dawnlight.lookup import ModelLookup
from zope.component.interfaces import IObjectEvent
from zope.event import notify
from zope.interface import Attribute, implementer

try:
    from .auth import security_check as component_protector
except:
    from cromlech.security import component_protector


class IModelFoundEvent(IObjectEvent):
    request = Attribute("The current request")


class IBeforeTraverseEvent(IObjectEvent):
    request = Attribute("The current request")


@implementer(IBeforeTraverseEvent)
class BeforeTraverseEvent(object):

    def __init__(self, ob, request):
        self.object = ob
        self.request = request


@implementer(IModelFoundEvent)
class ModelFoundEvent(object):

    def __init__(self, ob, request):
        self.object = ob
        self.request = request


class UVCModelLookup(ModelLookup):

    def __call__(self, request, obj, stack):
        """Traverses following stack components and starting from obj.
        """
        unconsumed = stack[:]
        while unconsumed:
            for consumer in self.lookup(obj):
                any_consumed, obj, unconsumed = consumer(
                    request, obj, unconsumed)
                if any_consumed:
                    notify(BeforeTraverseEvent(obj, request))
                    break
            else:
                break

        notify(ModelFoundEvent(obj, request))
        return obj, unconsumed


located_view = ViewLookup(view_locator(query_view))
secured_view = ViewLookup(component_protector(view_locator(query_view)))
base_model_lookup = UVCModelLookup()
