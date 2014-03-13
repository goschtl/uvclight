# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de

import json
import urllib
import xmlrpclib
from os import path
from dolmen.template import TALTemplate
from zope.security.management import getInteraction
from dolmen.location import get_absolute_url

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


def make_xmlrpc_response(view, result, name=None):
    return [xmlrpclib.dumps(tuple([result]),
            view.response, name, view.encoding, view.allownone)]


def current_principal():
    policy = getInteraction()
    if len(policy.participations) == 1:
        return policy.participations[0].principal
    return None


def url(request, obj, name=None, data=None):

    url = get_absolute_url(obj, request)
    if name is not None:
        url += '/' + urllib.quote(name.encode('utf-8'))

    if not data:
        return url

    if not isinstance(data, dict):
        raise TypeError('url() data argument must be a dict.')

    for k, v in data.items():
        if isinstance(v, unicode):
            data[k] = v.encode('utf-8')
        if isinstance(v, (list, set, tuple)):
            data[k] = [
                isinstance(item, unicode) and item.encode('utf-8')
                or item for item in v]

    return url + '?' + urllib.urlencode(data, doseq=True)
