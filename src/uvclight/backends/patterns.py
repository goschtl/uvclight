try:
    import traject
    from uvclight.directives import context, order
    from cromlech.browser import redirect_response
    from cromlech.webob import response
    from grokcore.component import Subscription
    from zope.interface import Interface, implements
    from dolmen.location import get_absolute_url
    from dawnlight.interfaces import IConsumer
    from dawnlight import ModelLookup
    

    def register_models(registry, *models):
        for model in models:
            pattern = model.pattern
            factory = model.factory.im_func
            arguments = model.arguments.im_func
            root = context.bind(default=Interface).get(model)
            registry.register(model.model, root, pattern, factory, arguments)


    class DefaultModel(object):

        def __init__(self, **kws):
            self.kws = kws

        
    def default_component(root, request):
        def factory(**kwargs):
            url = get_absolute_url(root, request)
            return redirect_response(response.Response, url)
        return factory

    
    class TrajectLookup(ModelLookup):

        def __init__(self, default=DefaultModel):
            self.patterns = traject.Patterns()
            self.default = default

        def register(self, model, root, pattern, factory, arguments):
            self.patterns.register(root, pattern, factory)
            self.patterns.register_inverse(root, model, pattern, arguments)

        def __call__(self, request, obj, stack):
            left = '/'.join((name for ns, name in reversed(stack)))
            unconsumed, consumed, obj = self.patterns.consume(
                obj, left, self.default)
            if consumed:
                return obj, stack[:-len(consumed)]
            return obj, stack


    class Model(object):
        context(Interface)

        model = None
        pattern = None

        def factory(*args):
            raise NotImplementedError

        def arguments(*args):
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
