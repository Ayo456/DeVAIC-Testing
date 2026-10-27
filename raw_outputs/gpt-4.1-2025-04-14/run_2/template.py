```python
def template(*args, **kwargs):
    global TEMPLATES, TEMPLATE_PATH, DEBUG
    tpl = args[0]
    var_dicts = args[1:]
    adapter = kwargs.pop('template_adapter', None) or SimpleTemplate
    lookup = kwargs.pop('template_lookup', None) or TEMPLATE_PATH
    settings = kwargs.pop('template_settings', None) or {}
    variables = dict(kwargs)
    for d in var_dicts:
        if d:
            variables.update(d)
    cache_key = (tuple(lookup), tpl)
    use_cache = not DEBUG
    template_obj = None
    if hasattr(tpl, 'render'):
        template_obj = tpl
        if settings:
            prepare = getattr(template_obj, 'prepare', None)
            if prepare:
                prepare(**settings)
    else:
        is_source = False
        if isinstance(tpl, str):
            if '\n' in tpl or any(c in tpl for c in ('{', '%', '$')):
                is_source = True
        if use_cache and cache_key in TEMPLATES:
            template_obj = TEMPLATES[cache_key]
        else:
            try:
                if is_source:
                    template_obj = adapter(source=tpl, lookup=lookup, **settings)
                else:
                    template_obj = adapter(name=tpl, lookup=lookup, **settings)
            except Exception:
                abort(500, f'Template ({tpl}) not found')
            if use_cache:
                TEMPLATES[cache_key] = template_obj
    try:
        return template_obj.render(variables)
    except Exception:
        abort(500, f'Template ({tpl}) not found')
```