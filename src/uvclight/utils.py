# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de

import json
import urllib
import xmlrpclib
from os import path

from cromlech.configuration.utils import load_zcml
from dolmen.location import get_absolute_url
from dolmen.template import TALTemplate
from zope.security.management import getInteraction
from GenericCache.GenericCache import GenericCache, default_marshaller
from GenericCache.GenericCache import cached

marker = object()
TEMPLATES_DIR = path.join(path.dirname(__file__), 'templates')
lineage_cache = GenericCache(expiry=3000, maxsize=5000)

    
def node_marshaller(func, node):
    return repr((func.__name__, node._p_oid))


@cached(lineage_cache, marshaller=node_marshaller)
def get_lineage(node):
    result = []
    while node is not None:
        result.append(node)
        node = getattr(node, '__parent__', None)
    return result


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


def eval_loader(expr):
    """load  a class / function

    :param expr: dotted name of the module ':' name of the class / function
    :raises RuntimeError: if expr is not a valid expression
    :raises ImportError: if module or object not found
    """
    modname, elt = expr.split(':', 1)
    if modname:
        try:
            module = __import__(modname, {}, {}, ['*'])
            val = getattr(module, elt, marker)
            if val is marker:
                raise ImportError('')
            return val
        except ImportError:
            raise ImportError(
                    "Bad specification %s: no item name %s in %s." %
                    (expr, elt, modname))
    else:
        raise RuntimeError("Bad specification %s: no module name." % expr)
