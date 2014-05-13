try:
    from cromlech.sqlalchemy import SQLAlchemySession
    from cromlech.sqlalchemy import create_and_register_engine, create_engine
    from dolmen.sqlcontainer import SQLContainer

except ImportError:
    print "SQL capabilities don't seem to be activated"
