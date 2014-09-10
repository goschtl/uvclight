try:
    import ZODB
    import cromlech.zodb

    from cromlech.zodb import Site, get_site
    from cromlech.zodb.middleware import ZODBApp
    from cromlech.zodb.utils import init_db
    from dolmen.container.components import BTreeContainer
    from dolmen.content import Model, Container, schema
    from persistent import Persistent
    from transaction import manager as transaction_manager
    from uvclight import events, components
    from zope.annotation.interfaces import IAttributeAnnotatable
    from zope.component import getGlobalSiteManager
    from zope.component.interfaces import ISite, IPossibleSite
    from zope.event import notify
    from zope.interface import implementer
    from zope.location import Location
    from zope.security.management import setSecurityPolicy


    @implementer(IAttributeAnnotatable)
    class Content(components.Content, Persistent):

        def __init__(self, **kwargs):
            Persistent.__init__(self)
            components.Content.__init__(self, **kwargs)


    @implementer(IAttributeAnnotatable)
    class Container(components.Container, BTreeContainer):

        def __init__(self, **kwargs):
            BTreeContainer.__init__(self)
            components.Container.__init__(self, **kwargs)


    class Root(BTreeContainer, cromlech.zodb.PossibleSite, Location):
        pass


    def make_application(name, model=Root):
        def create_app(db):
            conn = db.open()
            try:
                root = conn.root()
                if not name in root:
                    with transaction_manager:
                        app = root[name] = model()
                        if (not ISite.providedBy(app) and
                                IPossibleSite.providedBy(app)):
                            cromlech.zodb.LocalSiteManager(app)
                        notify(events.ApplicationInitializedEvent(app))
            finally:
                conn.close()
        return create_app


    class ZODBSecurePublication(SecurePublication):

        def __init__(self, session_key, environ_key, name, layers=None):
            SecurePublication.__init__(self, session_key, layers)
            self.environ_key = environ_key

        @classmethod
        def create(cls, session_key, environ_key, conf, name, root, secur):
            db = init_db(conf, make_application(name, root))
            app = cls(session_key, environ_key, name, layers=layers)
            return ZODBApp(app, db, key=environ_key)

        def site_manager(self, environ):
            conn = environ[self.environ_key]
            site = get_site(conn, self.name)
            return Site(site)
    

except ImportError:
    print "ZODB capabilities don't seem to be activated"
