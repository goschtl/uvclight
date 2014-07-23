# -*- coding: utf-8 -*-

from cromlech.dawnlight import DawnlightPublisher
from cromlech.dawnlight import ViewLookup
from cromlech.dawnlight import view_locator, query_view


def create_base_publisher():
    view_lookup = ViewLookup(view_locator(query_view))
    return DawnlightPublisher(view_lookup=view_lookup)
