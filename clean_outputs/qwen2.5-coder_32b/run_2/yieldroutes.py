def yieldroutes(func):
    if hasattr(func, '__wrapped__'):
        yield from yieldroutes(func.__wrapped__)
    elif hasattr(func, 'subroutes'):
        for route in func.subroutes:
            yield from yieldroutes(route.handler)
    else:
        yield func