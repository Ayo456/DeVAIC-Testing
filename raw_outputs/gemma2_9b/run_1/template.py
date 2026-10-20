```python
def template(tpl, *args, **kwargs):
  if isinstance(tpl, str):
    return tpl.format(*args, **kwargs)
  elif isinstance(tpl, (tuple, list)):
    return tpl[0].format(*args, **kwargs)
  else:
    return tpl.render(*args, **kwargs) 
```