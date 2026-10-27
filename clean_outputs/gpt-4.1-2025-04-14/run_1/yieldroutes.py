import inspect

def yieldroutes(func):
    sig = inspect.signature(func)
    params = list(sig.parameters.values())
    required = [p for p in params if p.default is inspect.Parameter.empty and p.kind in (p.POSITIONAL_OR_KEYWORD, p.POSITIONAL_ONLY)]
    optional = [p for p in params if p.default is not inspect.Parameter.empty and p.kind in (p.POSITIONAL_OR_KEYWORD, p.POSITIONAL_ONLY)]
    base = '/' + func.__name__.replace('__', '/').lstrip('/')
    path = base + ''.join((f'/<{p.name}>' for p in required))
    yield path
    for i in range(1, len(optional) + 1):
        path += f'/<{optional[i - 1].name}>'
        yield path