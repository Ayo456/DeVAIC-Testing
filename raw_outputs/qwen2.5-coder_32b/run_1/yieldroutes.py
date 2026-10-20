```python
def yieldroutes(func):
    if hasattr(func, '__wrapped__'):
        yield from yieldroutes(func.__wrapped__)
    elif hasattr(func, 'subroutes'):
        for subroute in func.subroutes:
            yield from yieldroutes(subroute.handler)
    else:
        yield func
```