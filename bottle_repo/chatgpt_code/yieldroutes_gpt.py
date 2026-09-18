def yieldroutes(func):
    if hasattr(func, "routes"):
        for route in func.routes:
            yield from yieldroutes(route)
        return

    if hasattr(func, "__wrapped__"):
        yield from yieldroutes(func.__wrapped__)
        return

    if hasattr(func, "callback"):
        yield from yieldroutes(func.callback)
        return

    yield func