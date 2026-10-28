def yieldroutes(func):
    name = func.__name__.replace('__', '/')
    args = func.__code__.co_varnames[:func.__code__.co_argcount]
    yield ('/' + name)
    for arg in args:
        if arg not in func.__defaults__:
            yield ('/' + name + '/' + arg)
    for arg in args:
        if arg in func.__defaults__:
            yield ('/' + name + '/' + '/'.join((arg for arg in args[:args.index(arg)])) + '/' + arg)