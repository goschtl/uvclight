try:
    import traject
    from cromlech.browser import redirect_response
    from cromlech.webob import response
    from grokcore.component import context, order, Subscription
    from zope.interface import Interface, implements
    from dolmen.location import get_absolute_url
    from dawnlight.interfaces import IConsumer
    from dawnlight import ModelLookup
    

    def register_models(registry, root, *models):
        for model in models:
            pattern = model.pattern
            factory = model.factory.im_func
            root = context.bind(default=Interface).get(model)
            registry.register(root, pattern, factory)


    def default_component(root, request):
        def factory(**kwargs):
            url = get_absolute_url(root, request)
            return redirect_response(response.Response, url)
        return factory

    
    class TrajectLookup(ModelLookup):

        def __init__(self):
            self.patterns = traject.Patterns()

        def register(self, root, pattern, factory):
            self.patterns.register(root, pattern, factory)

        def __call__(self, request, obj, stack):
            left = '/'.join((name for ns, name in reversed(stack)))
            Default = default_component(obj, request)
            unconsumed, consumed, obj = self.patterns.consume(
                obj, left, Default)
            if consumed:
                return obj, stack[:-len(consumed)]
            return obj, stack


    class DefaultModel(object):

        def __init__(self, **kw):
            self.kw = kw


    class Model(object):
        context(Interface)

        model = None
        pattern = None

        @staticmethod
        def factory(*args):
            raise NotImplementedError

        def arguments(inst):
            raise NotImplementedError


    class TrajectConsumer(Subscription):
        order(700)
        context(Interface)
        implements(IConsumer)

        def __call__(self, request, root, stack):
            left = '/'.join((name for ns, name in reversed(stack)))
            Default = default_component(root, request)
            unconsumed, consumed, obj = PATTERNS.consume(root, left, Default)
            if consumed:
                return True, obj, stack[:-len(consumed)]
            return False, obj, stack

        
except ImportError:
    print "Traject capabilities don't seem to be activated"
    raise
