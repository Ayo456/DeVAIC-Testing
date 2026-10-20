def template(tpl, *args, **kwargs):
    import os
    import jinja2
    if os.path.exists(tpl):
        env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(tpl)))
        template = env.get_template(os.path.basename(tpl))
    else:
        template = jinja2.Template(tpl)
    return template.render(*args, **kwargs)