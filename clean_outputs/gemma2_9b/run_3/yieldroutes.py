def yieldroutes(func):
    name = func.__name__.replace('__', '/')
    args = func.__code__.co_varnames[:func.__code__.co_argcount]
    yield ('/' + name)
    for i, arg in enumerate(args):
        if func.__defaults__[i] is None:
            yield ('/' + name + '/' + arg)
        else:
            yield ('/' + name + '/' + '/'.join(args[:i + 1]))