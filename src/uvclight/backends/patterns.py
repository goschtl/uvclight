try:
    import traject
    from grokcore.component import context, order, Subscription
    from zope.interface import Interface, implements
    from dolmen.location import get_absolute_url
    from dawnlight.interfaces import IConsumer

    
    PATTERNS = traject.Patterns()


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


    def register_pattern(root, *models):
        for model in models:
            pattern = model.pattern
            factory = model.factory
            root = context.bind(default=Interface).get(model)
            PATTERNS.register(root, pattern, factory)


    def default_component(root, request):
        def factory(**kwargs):
            url = get_absolute_url(root, request)
            return redirect_response(response.Response, url)
        return factory


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
