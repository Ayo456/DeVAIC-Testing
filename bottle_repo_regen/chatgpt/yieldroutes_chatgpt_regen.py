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

# regen 2
def yieldroutes(func):
    seen = set()

    def walk(obj):
        if id(obj) in seen:
            return

        seen.add(id(obj))

        for attr in ("routes", "children", "handlers"):
            nested = getattr(obj, attr, None)

            if nested:
                if isinstance(nested, dict):
                    nested = nested.values()

                for child in nested:
                    callback = getattr(child, "callback", child)
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

# regen 3
def yieldroutes(func):
    seen = set()

    def walk(obj):
        if id(obj) in seen:
            return

        seen.add(id(obj))

        for attr in ("routes", "children", "handlers"):
            nested = getattr(obj, attr, None)
            if nested:
                for child in nested:
                    yield from walk(child)
                return

        for attr in ("callback", "handler", "__wrapped__"):
            child = getattr(obj, attr, None)
            if child is not None and child is not obj:
                yield from walk(child)
                return

        if callable(obj):
            yield obj

    yield from walk(func)