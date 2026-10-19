import os
from jinja2 import Environment, FileSystemLoader, Template

def template(tpl, *args, **kwargs):
    env = Environment()
    if os.path.isfile(tpl):
        env = Environment(loader=FileSystemLoader(os.path.dirname(tpl)))
        template_name = os.path.basename(tpl)
        tmpl = env.get_template(template_name)
    else:
        tmpl = Template(tpl)
    return tmpl.render(*args, **kwargs)