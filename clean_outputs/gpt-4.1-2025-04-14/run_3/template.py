def template(*args, **kwargs):
    global TEMPLATES, TEMPLATE_PATH, DEBUG
    if not args:
        abort(500, 'Template (None) not found')
    tpl_arg = args[0]
    var_dicts = args[1:]
    adapter = kwargs.pop('template_adapter', SimpleTemplate)
    lookup = kwargs.pop('template_lookup', TEMPLATE_PATH)
    settings = kwargs.pop('template_settings', {})
    for d in var_dicts:
        if d:
            kwargs.update(d)
    is_str = isinstance(tpl_arg, str)
    if is_str and ('\n' in tpl_arg or '{' in tpl_arg or '%' in tpl_arg or ('$' in tpl_arg)):
        tpl_type = 'source'
    elif is_str:
        tpl_type = 'name'
    else:
        tpl_type = 'object'
    cache_key = (tuple(lookup) if isinstance(lookup, (list, tuple)) else (lookup,), tpl_arg)
    tpl = None
    if tpl_type == 'object':
        tpl = tpl_arg
        if settings:
            if hasattr(tpl, 'prepare'):
                tpl.prepare(**settings)
    elif not DEBUG and cache_key in TEMPLATES:
        tpl = TEMPLATES[cache_key]
    else:
        try:
            if tpl_type == 'source':
                tpl = adapter(source=tpl_arg, lookup=lookup, **settings)
            else:
                tpl = adapter(name=tpl_arg, lookup=lookup, **settings)
        except Exception:
            abort(500, f'Template ({tpl_arg}) not found')
        if not DEBUG:
            TEMPLATES[cache_key] = tpl
    if not tpl:
        abort(500, f'Template ({tpl_arg}) not found')
    return tpl.render(kwargs)