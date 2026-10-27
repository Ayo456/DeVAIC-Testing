```python
def template(*args, **kwargs):
  tpl_name = args[0]
  if isinstance(tpl_name, str):
    if '\n' in tpl_name or any(c in tpl_name for c in ('{', '%', '$')):
      tpl_source = tpl_name
    else:
      tpl_source = None
      tpl_name = tpl_name
  else:
    tpl_source = None
  
  if DEBUG:
    TEMPLATES = {}
  if tpl_source is not None:
    key = (TEMPLATE_PATH, tpl_source)
    if key in TEMPLATES:
      tpl = TEMPLATES[key]
    else:
      tpl = adapter(source=tpl_source, lookup=TEMPLATE_PATH, **kwargs.get('template_settings', {}))
      TEMPLATES[key] = tpl
  else:
    key = (TEMPLATE_PATH, tpl_name)
    if key in TEMPLATES:
      tpl = TEMPLATES[key]
    else:
      tpl = adapter(name=tpl_name, lookup=TEMPLATE_PATH, **kwargs.get('template_settings', {}))
      TEMPLATES[key] = tpl

  merged_vars = kwargs.copy()
  for i in range(1, len(args)):
    merged_vars.update(args[i])
  
  return tpl.render(merged_vars)
```