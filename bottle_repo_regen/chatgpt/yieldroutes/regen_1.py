# regen 1
def yieldroutes(func):
    seen = set()

    def walk(obj):
        if id(obj) in seen:
            return

        seen.add(id(obj))

        routes = getattr(obj, "routes", None)

        if routes:
            for route in routes:
                callback = getattr(route, "callback", route)
                yield from walk(callback)
            return

        wrapped = getattr(obj, "__wrapped__", None)

        if wrapped is not None:
            yield from walk(wrapped)
            return

        callback = getattr(obj, "callback", None)

        if callback is not None and callback is not obj:
            yield from walk(callback)
            return

        if callable(obj):
            yield obj

    yield from walk(func)
