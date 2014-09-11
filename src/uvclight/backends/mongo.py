try:
    from pymongo import MongoClient
    from cromlech.browser.interfaces import IPublicationRoot
    from zope.interface import implementer
    from zope.location import Location


    class Collection(object):
        """Abstraction object to represent and handle Mongo Collections.
        """
        
        def __init__(self, manager, path):
            self.path = path
            self.manager = manager

        def get_docs(self, *filters):
            results = self.manager(*filters)
            return map(doc_marshaller, result)


    class Container(Location):

        def __init__(self, collection):
            self.collection = collection
        
        def __getitem__(self, name):
            return self.collection.get(name)


    @implementer(IPublicationRoot)
    class Root(Location, dict):

        def __init__(self, session):
            self.session = session

        def add(self, collection, ):
            

    def connect(dsn=None, auto_start_request=False):
        if dsn is not None:
            return MongoClient(dsn, auto_start_request=auto_start_request)
        return MongoClient(auto_start_request=auto_start_request)


    class MongoDBIndexer(object):

        def __init__(self, client, collection):
            self.client = client
            self.collection = collection

        def indexDoc(self, *datas):
            with self.client.start_request():
                self.collection.insert(*datas)
            self.collection.ensure_index("state")

        def reindexDoc(self, *datas):
            with self.client.start_request():
                for data in datas:
                    self.collection.save(data)

        def unindexDoc(self, *datas):
            with self.client.start_request():
                for data in datas:
                    self.collection.remove(data, True)

        def listDocs(self, *args, **kwargs):
            """Override this method to work on filters.
            """
            filters = {}
            with self.client.start_request():
                docs = self.collection.find(**filters)
            return list(docs)

        def purge(self):
            """Use with care.
            """
            self.collection.remove()


except ImportError:
    print "MongoDB capabilities don't seem to be activated"
