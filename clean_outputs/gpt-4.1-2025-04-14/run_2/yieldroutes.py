import inspect

def yieldroutes(func):
    sig = inspect.signature(func)
    params = list(sig.parameters.values())
    required = []
    optional = []
    for p in params:
        if p.default is inspect.Parameter.empty and p.kind in (p.POSITIONAL_OR_KEYWORD, p.POSITIONAL_ONLY, p.KEYWORD_ONLY):
            required.append(p.name)
        elif p.kind in (p.POSITIONAL_OR_KEYWORD, p.POSITIONAL_ONLY, p.KEYWORD_ONLY):
            optional.append(p.name)
    base = '/' + func.__name__.replace('__', '/').lstrip('/')
    segs = ['/<{}>'.format(name) for name in required]
    yield (base + ''.join(segs))
    path = base + ''.join(segs)
    for i, name in enumerate(optional):
        path += '/<{}>'.format(name)
        yield path