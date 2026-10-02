# regen 3
def template(tpl, *args, **kwargs):
    adapter = kwargs.pop("template_adapter", SimpleTemplate)
    lookup = kwargs.pop("template_lookup", TEMPLATE_PATH)
    settings = kwargs.pop("template_settings", {})

    if tpl not in TEMPLATES or DEBUG:
        if isinstance(tpl, adapter):
            TEMPLATES[tpl] = tpl
        elif "\n" in tpl or "{" in tpl or "%" in tpl or "$" in tpl:
            TEMPLATES[tpl] = adapter(source=tpl, lookup=lookup, **settings)
        else:
            TEMPLATES[tpl] = adapter(name=tpl, lookup=lookup, **settings)

    for arg in args:
        if isinstance(arg, dict):
            kwargs.update(arg)

    return TEMPLATES[tpl].render(**kwargs)
