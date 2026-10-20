def yieldroutes(func):
    if hasattr(func, '__call__'):
        for attr in dir(func):
            if callable(getattr(func, attr)) and attr != '__call__':
                yield from yieldroutes(getattr(func, attr))
        yield func