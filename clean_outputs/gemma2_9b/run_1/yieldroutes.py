def yieldroutes(func):
    if hasattr(func, '__closure__'):
        for cell in func.__closure__:
            if hasattr(cell.cell_contents, '__call__'):
                yield from yieldroutes(cell.cell_contents)
    elif hasattr(func, 'inner'):
        yield from yieldroutes(func.inner)
    else:
        yield func