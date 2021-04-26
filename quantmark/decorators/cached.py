import functools


def cached(function):
	"""An attempt to fix the functools.lru_cahche in python 3.7)."""
	@functools.lru_cache(maxsize=30)
	def cache(function, *args, **kwargs):
		return function(*args, **kwargs)

	@functools.wraps(function)
	def wrapper(*args, **kwargs):
		return cache(function, *args, **kwargs)

	return wrapper
