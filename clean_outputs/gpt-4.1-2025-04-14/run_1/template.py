def template(*args, **kwargs):
    global TEMPLATES, TEMPLATE_PATH, DEBUG
    if not args:
        abort(500, 'Template (None) not found')
    tpl = args[0]
    vars_dict = dict(kwargs)
    for d in args[1:]:
        if isinstance(d, dict):
            vars_dict.update(d)
    adapter = vars_dict.pop('template_adapter', None) or SimpleTemplate
    lookup = vars_dict.pop('template_lookup', None) or TEMPLATE_PATH
    settings = vars_dict.pop('template_settings', None) or {}
    cache_key = (tuple(lookup), tpl)
    template_obj = None
    if hasattr(tpl, 'render'):
        template_obj = tpl
        if settings:
            prepare = getattr(template_obj, 'prepare', None)
            if callable(prepare):
                prepare(**settings)
    else:
        is_source = False
        if isinstance(tpl, str):
            if any((c in tpl for c in ('\n', '{', '%', '$'))):
                is_source = True
        if not DEBUG and cache_key in TEMPLATES:
            template_obj = TEMPLATES[cache_key]
        else:
            try:
                if is_source:
                    template_obj = adapter(source=tpl, lookup=lookup, **settings)
                else:
                    template_obj = adapter(name=tpl, lookup=lookup, **settings)
            except Exception:
                abort(500, f'Template ({tpl}) not found')
            if not DEBUG:
                TEMPLATES[cache_key] = template_obj
    if not template_obj:
        abort(500, f'Template ({tpl}) not found')
    return template_obj.render(vars_dict)