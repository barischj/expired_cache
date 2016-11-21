# expired_cache

A cache which returns an expired value while the value is being updated.

The cached value of `fn(a, k)` is only updated when that call is made and the
cached value has existed for `ttl` seconds, not as soon as the cached value
expires.

The cached value is updated in another thread. The cache doesn't wait for the
fresh value to be computed but instead returns the expired value.

This means that while a call might return an expired value, as many calls as
possible will return without waiting for the cached value to be updated. The
exception is when the cached value doesn't exist yet. Ensure the cached value
is computed as soon as possible make a call when the module is imported.
