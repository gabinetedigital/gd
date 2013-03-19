# -*- coding: UTF-8 -*-
"""
This is a util methods to work with flask-cache.
how-to:

variable = fromcache('<cachekey>') or tocache('<cachekey>', <live-object> )

print variable

"""
from gd.content import cache

def fromcache(name):
	o = cache.get(name)
	if o:
		return o
		print "FromCache:%s" % name
	else:
		return False

def tocache(name, obj):
	global cache
	cache.add(name, obj)
	print "ToCache:%s" % name
	print dir(cache)
	return obj
