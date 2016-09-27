import pylru
import threading
import time


def Cache(object):

    def __init__(self, ttl, max_size):
        self.ttl = ttl  # seconds
        self.cache = pylru.lrucache(max_size)  # {key: (expires, value)}
        lock = threading.Lock()

    def _update(self, key, fn, args, kwargs):
        """Returns the newly set cached value."""
        value = fn(*args, **kwargs)
        self.cache[key] = (time.time() + self.ttl, value)
        return value

    def get(self, fn, args, kwargs):
        """Returns the currently cached copy."""
        key = (args, kwargs)
        # If there exists a cached value.
        if key in self.cache:
            (expires, value) = lru_cache[key]
            # Update cached value if expired and not already being updated...
            if expires > time.time() and update_lock.acquire(blocking=False):
                def update_and_release():
                    try:
                        self._update(key, fn, args, kwargs)
                    finally:
                        update_lock.release()
                threading.Thread(target=update_and_release).start()
            # ...but still return expired copy.
            return value
        # Else cache and return a new value.
        return self._update(key, fn, args, kwargs)


def cache(ttl, max_size=128):
    cache = Cache(max_size)
    def decorator(original_fn):
        def new_fn(*args, **kwargs):
            return cache.get(original_fn, args, kwargs)
        return new_fn
    return decorator
