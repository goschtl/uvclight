try:
    import cromlech.zodb

    from ..bricks import SecurePublication
    from cromlech.zodb import Site, get_site
    from cromlech.zodb.middleware import ZODBApp
    from cromlech.zodb.utils import init_db
    from dolmen.container.components import BTreeContainer
    from persistent import Persistent
    from transaction import manager as transaction_manager
    from uvclight import events, components
    from zope.annotation.interfaces import IAttributeAnnotatable
    from zope.component.interfaces import ISite, IPossibleSite
    from zope.event import notify
    from zope.interface import implementer
    from zope.location import Location
    from uvclight.utils import with_zcml, with_i18n
    from ..bricks import Publication


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


    class ZODBPublication(Publication):
        """Publication mixin
        """

        @classmethod
        def create(cls, session_key='session.key', environ_key='zodb.key',
                   conf=None, name='app', root=None):
            db = init_db(conf, make_application(name, root))
            app = cls(session_key, environ_key, name)
            return ZODBApp(app, db, key=environ_key)

        def __init__(self, session_key, environ_key, name):
            self.session_key = session_key
            self.environ_key = environ_key
            self.name = name
            self.publish = self.get_publisher()

        def site_manager(self, environ):
            conn = environ[self.environ_key]
            site = get_site(conn, self.name)
            return Site(site)


except ImportError:
    print "ZODB capabilities don't seem to be activated"
