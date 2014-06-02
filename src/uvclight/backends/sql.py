try:
    import transaction
    from cromlech.sqlalchemy import SQLAlchemySession
    from cromlech.sqlalchemy import create_and_register_engine, create_engine
    from dolmen.sqlcontainer import SQLContainer
    
    def transaction_sql(engine):
        def sql_wrapped(wrapped):
            def caller(environ, start_response):
                with transaction.manager as tm:
                    with SQLAlchemySession(engine, transaction_manager=tm):
                        return wrapped(environ, start_response)
            return caller
        return sql_wrapped

except ImportError:
    raise
    print "SQL capabilities don't seem to be activated"
