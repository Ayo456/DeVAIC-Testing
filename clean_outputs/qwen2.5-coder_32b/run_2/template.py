import os
from string import Template

def template(tpl, *args, **kwargs):
    if os.path.isfile(tpl):
        with open(tpl, 'r') as file:
            tpl = file.read()
    tmpl = Template(tpl)
    return tmpl.substitute(*args, **kwargs)