# -*- coding: UTF-8 -*-
"""
This is a util methods to work with flask-cache.
how-to:

variable = fromcache('<cachekey>') or tocache('<cachekey>', <live-object> )

print variable

"""
from flask.ext.cache import Cache
cache = Cache()
cache.CACHE_DEFAULT_TIMEOUT = 600 #10 minutos

def fromcache(name):
	o = cache.get(name)
	if o:
		return o
	else:
		return False

def tocache(name, obj):
	global cache
	cache.add(name, obj)
	return obj

def removecache(name):
	global cache
	cache.delete(name)
