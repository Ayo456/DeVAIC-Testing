def template(tpl, *args, **kwargs):
    if isinstance(tpl, str):
        return tpl.format(*args, **kwargs)
    return tpl.render(*args, **kwargs)