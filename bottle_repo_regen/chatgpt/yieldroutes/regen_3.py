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
