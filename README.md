# expired-cache

Return the cached value while the new value is being calculated. This has the
benfit that if the calculation takes a long time we don't have to wait for the
calculation to finish to return a value. The exception being when a cached value
doesn't exist yet, to remedy this make a call as early as possible to have a
cached value is calculated.

The cached value `fn(...)` is recalculated when a call to `fn` is made and the
previously calculated value has existed for `ttl` seconds.
