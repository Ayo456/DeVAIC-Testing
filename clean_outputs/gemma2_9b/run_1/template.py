def template(*args, **kwargs):
    tpl_name = args[0]
    if isinstance(tpl_name, str):
        if '\n' in tpl_name or any((c in tpl_name for c in ('{', '%', '$'))):
            tpl_source = tpl_name
        else:
            tpl_source = None
            tpl_name = tpl_name
    else:
        tpl_source = None
    args = args[1:]
    variables = {}
    for arg in args:
        variables.update(arg)
    template_adapter = kwargs.pop('template_adapter', SimpleTemplate)
    template_lookup = kwargs.pop('template_lookup', TEMPLATE_PATH)
    template_settings = kwargs.pop('template_settings', {})
    if DEBUG:
        if tpl_source is not None:
            if tpl_source not in TEMPLATES:
                TEMPLATES[template_lookup, tpl_source] = template_adapter(source=tpl_source, lookup=template_lookup, **template_settings)
        elif (template_lookup, tpl_name) not in TEMPLATES:
            TEMPLATES[template_lookup, tpl_name] = template_adapter(name=tpl_name, lookup=template_lookup, **template_settings)
    elif tpl_source is not None:
        if (template_lookup, tpl_source) not in TEMPLATES:
            TEMPLATES[template_lookup, tpl_source] = template_adapter(source=tpl_source, lookup=template_lookup, **template_settings)
    elif (template_lookup, tpl_name) not in TEMPLATES:
        TEMPLATES[template_lookup, tpl_name] = template_adapter(name=tpl_name, lookup=template_lookup, **template_settings)
    if tpl_source is not None:
        tpl = TEMPLATES[template_lookup, tpl_source]
    else:
        tpl = TEMPLATES[template_lookup, tpl_name]
    return tpl.render(variables)