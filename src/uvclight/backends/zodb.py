try:
    import ZODB
    import cromlech.zodb

    from dolmen.container.components import BTreeContainer
    from dolmen.content import Model, Container, schema
    from transaction import manager as transaction_manager
    from uvclight import events
    from zope.component import getGlobalSiteManager
    from zope.component.interfaces import ISite, IPossibleSite
    from zope.event import notify
    from zope.location import Location


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

        

except ImportError:
    print "ZODB capabilities don't seem to be activated"
