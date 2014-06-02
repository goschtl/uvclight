try:
    import transaction
    from cromlech.sqlalchemy import SQLAlchemySession

    def transaction_sql(engine):
        def sql_wrapped(wrapped):
            def caller(environ, start_response):
                with transaction.manager as tm:
                    with SQLAlchemySession(engine, transaction_manager=tm):
                        return wrapped(environ, start_response)
            return caller
        return sql_wrapped

except ImportError:
    print "SQL capabilities don't seem to be activated"
