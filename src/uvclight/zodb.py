try:
    import ZODB
    import cromlech.zodb



except ImportError:
    print "ZODB capabilities don't seem to be activated"
