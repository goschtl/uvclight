try:
    from ul.sql import *
except ImportError as exc:
    print exc
    print "SQL capabilities don't seem to be activated"
