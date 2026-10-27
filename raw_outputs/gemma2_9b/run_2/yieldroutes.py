```python
def yieldroutes(func):
  name = func.__name__.replace("__", "/")
  args = func.__code__.co_varnames[:func.__code__.co_argcount]
  yield "/" + name
  for arg in args:
    if func.__dict__.get(arg) is None:
      yield "/" + name + "/" + arg
  for arg in args:
    if func.__dict__.get(arg) is not None:
      yield "/" + name + "/" + "/".join([a for a in args if func.__dict__.get(a) is not None])
```