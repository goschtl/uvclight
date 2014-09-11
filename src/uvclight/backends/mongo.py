try:
    import pymongo

    # pyflakes bypass : work in progress
    pymongo

except ImportError:
    print "MongoDB capabilities don't seem to be activated"
