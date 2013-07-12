# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de

from os import path
from dolmen.template import TALTemplate


TEMPLATES_DIR = path.join(path.dirname(__file__), 'templates')


def get_template(filename, dir=None):
    if dir:
        return TALTemplate(path.join(path.dirname(dir), 'templates', filename))
    return TALTemplate(path.join(TEMPLATES_DIR, filename))
