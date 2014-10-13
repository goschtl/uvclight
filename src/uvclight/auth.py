try:
    from ul.auth import *
    from grokcore.security import Permission, require
    
except Exception, exc:
    print exc
    print "The Auth module doesn't seem to be available."
    raise
