from jinja2 import Template, Environment, FileSystemLoader

def template(tpl, *args, **kwargs):
    if isinstance(tpl, str):
        try:
            env = Environment(loader=FileSystemLoader('.'))
            tpl = env.get_template(tpl)
        except FileNotFoundError:
            tpl = Template(tpl)
    return tpl.render(*args, **kwargs)
template_string = 'Hello, {{ name }}! You are {{ age }} years old.'
rendered_string = template(template_string, name='Alice', age=30)
print(rendered_string)
file_template = 'template.html'
rendered_from_file = template(file_template, username='Bob')
print(rendered_from_file)