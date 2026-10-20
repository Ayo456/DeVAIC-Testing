def yieldroutes(func):
    if hasattr(func, '__call__'):
        for attr in dir(func):
            if attr != '__call__' and hasattr(getattr(func, attr), '__call__'):
                yield from yieldroutes(getattr(func, attr))
        yield func