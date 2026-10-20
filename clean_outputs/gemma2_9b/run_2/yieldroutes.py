def yieldroutes(func):
    if hasattr(func, '__call__'):
        for attr in dir(func):
            if callable(getattr(func, attr)):
                yield from yieldroutes(getattr(func, attr))
    yield func