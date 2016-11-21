import pylru
import threading
import time


def Cache(object):

    def __init__(self, ttl, max_size):
        self._ttl = ttl  # seconds
        self._cache = pylru.lrucache(max_size)  # {key: (expires, value)}
        self._lock = threading.Lock()

    def _update(self, key, fn, args, kwargs):
        """Updates a cached value."""
        fresh_value = fn(*args, **kwargs)
        self._cache[key] = (time.time() + self._ttl, fresh_value)

    def get(self, fn, args, kwargs):
        """Returns a cached value."""
        key = (args, kwargs)
        if key in self.cache:
            (expires, value) = self._cache[key]
            # If cached value is expired and not already being updated
            if expires > time.time() and self._lock.acquire(blocking=False):
                def update_and_release():
                    try:
                        self._update(key, fn, args, kwargs)
                    finally:
                        self._lock.release()
                threading.Thread(target=update_and_release).start()
            return value
        self._update(key, fn, args, kwargs)
        return self._cache[key]


def cache(*cache_args):
    cache = Cache(*cache_args)
    def wrapper(original_fn):
        def new_fn(*args, **kwargs):
            return cache.get(original_fn, *args, **kwargs)
        return new_fn
    return wrapper
