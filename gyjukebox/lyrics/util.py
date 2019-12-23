class Peekable:
    def __init__(self, iterable):
        self._iter = iter(iterable)
        self._cache = []

    def __next__(self):
        if self._cache:
            return self._cache.pop()
        return next(self._iter)

    def peek(self):
        assert len(self._cache) <= 1
        if self._cache:
            return self._cache[0]
        self._cache.append(next(self._iter))
        return self._cache[0]
