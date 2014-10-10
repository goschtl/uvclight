try:
    from ul.zodb import *
except ImportError as exc:
    print exc
    print "ZODB capabilities don't seem to be activated"
