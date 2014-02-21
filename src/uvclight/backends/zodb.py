try:
    import ZODB
    import cromlech.zodb

    from zope.location import Location
    from zope.component import getGlobalSiteManager
    from dolmen.container.components import BTreeContainer

    from dolmen.content import Model, Container, schema

    class Root(BTreeContainer, cromlech.zodb.PossibleSite, Location):

        def getSiteManager(self):
            return getGlobalSiteManager()


except ImportError:
    print "ZODB capabilities don't seem to be activated"
