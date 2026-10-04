def yieldroutes(func):
    if hasattr(func, '__closure__'):
        for cell in func.__closure__:
            if hasattr(cell.cell_contents, 'func'):
                yield from yieldroutes(cell.cell_contents.func)
    elif hasattr(func, '__wrapped__'):
        yield from yieldroutes(func.__wrapped__)
    else:
        yield func