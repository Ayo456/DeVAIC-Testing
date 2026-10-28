def yieldroutes(func):
    import inspect
    sig = inspect.signature(func)
    base_path = '/' + func.__name__.replace('__', '/')
    params = list(sig.parameters.values())
    required_params = [p.name for p in params if p.default == inspect.Parameter.empty]
    optional_params = [p.name for p in params if p.default != inspect.Parameter.empty]
    path = base_path + ''.join((f'/<{p}>' for p in required_params))
    yield path
    for i in range(len(optional_params)):
        path += f'/<{optional_params[i]}>'
        yield path