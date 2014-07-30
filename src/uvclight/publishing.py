# -*- coding: utf-8 -*-

from cromlech.dawnlight import DawnlightPublisher
from cromlech.dawnlight import ViewLookup
from cromlech.dawnlight import view_locator, query_view

try:
    from .auth import security_check as component_protector
except:
    from cromlech.security import component_protector


def create_base_publisher(secure=False):
    fetcher = query_view
    if secure:
        fetcher = component_protector(fetcher)
    fetcher = view_locator(fetcher)
    view_lookup = ViewLookup(fetcher)
    return DawnlightPublisher(view_lookup=view_lookup)
