def yield_routes(func):
    if hasattr(func, '__wrapped__'):
        func = func.__wrapped__
    if isinstance(func, type) or not callable(func):
        yield func
        return
    try:
        for line in func.__code__.co_code.decode('utf-8').splitlines():
            if line.startswith('route('):
                yield_routes(eval(line.split('route(')[1].rstrip('),').strip()))
    except (AttributeError, SyntaxError, NameError):
        yield func