try:
    from ul.traject.model import (
        DefaultModel,
        Model,
        default_component,
        register_models,
        )

    from ul.traject.publication import (
        TrajectLookup,
        )

    from ul.traject.consume import (
        TrajectConsumer,
        )

    
except ImportError:
    print "Traject capabilities don't seem to be activated"
    raise
