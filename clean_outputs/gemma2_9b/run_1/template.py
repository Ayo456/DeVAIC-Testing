from jinja2 import Template, Environment, FileSystemLoader

def template(tpl, *args, **kwargs):
    if isinstance(tpl, str):
        if tpl.startswith('template://'):
            with open(tpl[11:], 'r') as f:
                tpl = Template(f.read())
        else:
            env = Environment(loader=FileSystemLoader('.'))
            tpl = env.get_template(tpl)
    elif isinstance(tpl, Template):
        pass
    else:
        raise ValueError('Invalid template type. Must be a string, file path, or Jinja2 Template object.')
    return tpl.render(*args, **kwargs)