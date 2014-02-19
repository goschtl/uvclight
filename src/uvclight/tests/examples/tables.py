# -*- coding: utf-8 -*-
# Copyright (c) 2007-2013 NovaReto GmbH
# cklinger@novareto.de


import uvclight

from grokcore.component import Context


class TableView(uvclight.TableView):
    uvclight.context(Context)

    @property
    def values(self):
        return range(10)


class TablePage(uvclight.TablePage):
    uvclight.context(Context)

    @property
    def values(self):
        return (1, 2, 3)


class IdColumn(uvclight.Column):
    header = u"ID Column"
    id = "id_id"

    def renderCell(self, item):
        return item


class SpecialColumn(uvclight.Column):
    uvclight.view(TablePage)
    header = u"Special Column"
    id = "special_id"

    def renderCell(self, item):
        return item
