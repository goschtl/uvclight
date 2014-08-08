# -*- coding: utf-8 -*-

from cromlech.dawnlight import DawnlightPublisher
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


def create_base_publisher(secure=False):
    fetcher = view_locator(query_view)
    if secure:
        fetcher = component_protector(fetcher)
    view_lookup = ViewLookup(fetcher)
    return DawnlightPublisher(
        model_lookup=UVCModelLookup(), view_lookup=view_lookup)
