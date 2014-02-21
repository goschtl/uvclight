# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de

import json
from os import path
from dolmen.template import TALTemplate
from zope.security.management import getInteraction


TEMPLATES_DIR = path.join(path.dirname(__file__), 'templates')


def get_template(filename, dir=None):
    if dir:
        return TALTemplate(path.join(path.dirname(dir), 'templates', filename))
    return TALTemplate(path.join(TEMPLATES_DIR, filename))


def make_json_response(view, result, name=None):
    json_result = json.dumps(result)
    response = view.responseFactory()
    response.write(json_result)
    response.headers['Content-Type'] = 'application/json'
    return response


def current_principal():
    policy = getInteraction()
    if len(policy.participations) == 1:
        return policy.participations[0].principal
    return None
