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
    
    key = (kwargs.get('template_lookup', TEMPLATE_PATH), tpl_name)
    if key in TEMPLATES:
        tpl = TEMPLATES[key]
    else:
        if tpl_source is not None:
            tpl = adapter(source=tpl_source, lookup=kwargs.get('template_lookup', TEMPLATE_PATH), **kwargs.get('template_settings', {}))
        else:
            tpl = adapter(name=tpl_name, lookup=kwargs.get('template_lookup', TEMPLATE_PATH), **kwargs.get('template_settings', {}))
        TEMPLATES[key] = tpl
    
    del kwargs['template_adapter']
    del kwargs['template_lookup']
    del kwargs['template_settings']
    return tpl.render(**kwargs)
```