import os
from jinja2 import Environment, FileSystemLoader, Template

def template(tpl, *args, **kwargs):
    env = Environment()
    if os.path.isfile(tpl):
        with open(tpl, 'r') as file:
            template_str = file.read()
        template = Template(template_str)
    elif os.path.isdir(tpl):
        env = Environment(loader=FileSystemLoader(tpl))
        template_name = kwargs.pop('template_name', 'default.html')
        template = env.get_template(template_name)
    else:
        template = Template(tpl)
    return template.render(*args, **kwargs)