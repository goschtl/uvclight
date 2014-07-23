# -*- coding: utf-8 -*-

import dawnlight
from SimpleXMLRPCServer import SimpleXMLRPCDispatcher  
from cromlech.webob.request import Request
from zope.component import getMultiAdapter
from .interfaces import IXMLRPCView
from cromlech.dawnlight.utils import safe_path


def XMLRPCViewLookup(request, context, stack):
    size = len(stack)
    if size == 0:
        raise RuntimeError('No XMLRPC view by default')
    elif size > 1:
        raise RuntimeError("Couldn't resolve an XMLRPC View on %r" % context)
    else:
        namespace, viewname = stack[0]
        view = getMultiAdapter((context, request), IXMLRPCView, name=viewname)
        return view, None


def handle_xmplrpc_request(dispatcher, environ, start_response):
    try:
        length = int(environ['CONTENT_LENGTH'])
        data = environ['wsgi.input'].read(length)
        response = dispatcher._marshaled_dispatch(
            data, getattr(dispatcher, '_dispatch', None))
        response += '\n'
    except:
        start_response("500 Server error", [('Content-Type', 'text/plain')])
        return []
    else:
        start_response("200 OK", [('Content-Type','text/xml'),
                                  ('Content-Length', str(len(response)),)])
        return [response]


xmlrpcview_lookup = XMLRPCViewLookup


class XMLRPCApp(object):

    def __init__(self, root, model_lookup, view_lookup=xmlrpcview_lookup):
        self.root = root
        self.model_lookup = model_lookup
        self.view_lookup = view_lookup

    def __call__(self, environ, start_response):

        def safe_unicode(str, enc='utf-8'):
            if isinstance(str, unicode):
                return str
            return unicode(str, enc)
        
        def base_path(request):
            path = safe_path(request.path)
            script_name = safe_unicode(request.script_name)
            if path.startswith(script_name):
                return path[len(script_name):]
            return path

        request = Request(environ)
        path = base_path(request)
        stack = dawnlight.parse_path(path)
        obj, unconsumed = self.model_lookup(request, self.root, stack)
        view, leftover = self.view_lookup(request, obj, unconsumed)

        dispatcher = SimpleXMLRPCDispatcher(allow_none=True, encoding=None)
        dispatcher.register_introspection_functions()
        dispatcher.register_instance(view)

        return handle_xmplrpc_request(dispatcher, environ, start_response)
