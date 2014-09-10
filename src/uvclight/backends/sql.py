try:
    import transaction

    from ..bricks import SecurePublication
    from cromlech.sqlalchemy import SQLAlchemySession
    from cromlech.sqlalchemy import create_and_register_engine, create_engine
    from dolmen.sqlcontainer import SQLContainer
    from sqlalchemy_imageattach import context as store
    from sqlalchemy_imageattach.stores.fs import HttpExposedFileSystemStore
    from uvclight.backends.patterns import TrajectLookup


    def transaction_sql(engine):
        def sql_wrapped(wrapped):
            def caller(environ, start_response):
                with transaction.manager as tm:
                    with SQLAlchemySession(engine, transaction_manager=tm):
                        return wrapped(environ, start_response)
            return caller
        return sql_wrapped


    def sql_storage(fs_store):
        def sql_store(wrapped):
            def caller(environ, start_response):
                if fs_store is not None:
                    with store.store_context(fs_store):
                        return wrapped(environ, start_response)
                return wrapped(environ, start_response)
            return caller
        return sql_store


    class SQLSecurePublication(SecurePublication):

        def __init__(self, session_key, engine, fs_store=None, layers=None):
            self.layers = layers or list()
            self.publish = self.get_publisher()
            self.session_key = session_key
            self.engine = engine
            self.fs_store = fs_store

        @classmethod
        def create(cls, dsn, name, base, store_root=None, store_prefix=None):

            # We register our SQLengine under a given name
            engine = create_and_register_engine(dsn, name)
            engine.bind(base)

            # We create it all
            metadata = base.metadata
            metadata.create_all(engine.engine, checkfirst=True)

            if store_root is not None:
                fs_store = HttpExposedFileSystemStore(store_root, store_prefix)
                app = cls(session_key, engine, fs_store, layers)
                return fs_store.wsgi_middleware(app)
            else:
                app = cls(session_key, engine, fs_store=None, layers=layers)
                return app

        def __call__(self, environ, start_response):

            @transaction_sql(self.engine)
            @sql_storage(self.fs_store)
            def publish(environ, start_response):
                return SecurePublication.__call__(
                    self, environ, start_response)

            return publish(environ, start_response)


except ImportError:
    print "SQL capabilities don't seem to be activated"
