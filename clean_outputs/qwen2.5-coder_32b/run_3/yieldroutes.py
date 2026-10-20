def yieldroutes(func):
    if hasattr(func, '__wrapped__'):
        yield from yieldroutes(func.__wrapped__)
    elif hasattr(func, 'routes'):
        for route in func.routes:
            yield from yieldroutes(route.handler)
    else:
        yield func