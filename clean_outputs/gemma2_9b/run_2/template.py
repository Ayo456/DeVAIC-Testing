from jinja2 import Template, Environment, FileSystemLoader

def template(tpl, *args, **kwargs):
    if isinstance(tpl, str):
        env = Environment(loader=StringLoader([tpl]))
        template = env.get_template(tpl)
    elif isinstance(tpl, (str, Path)):
        env = Environment(loader=FileSystemLoader('.'))
        template = env.get_template(tpl)
    else:
        raise TypeError('Template must be a string or file path.')
    return template.render(*args, **kwargs)
template_str = 'Hello, {{ name }}! You are {{ age }} years old.'
rendered_str = template(template_str, name='Alice', age=30)
print(rendered_str)
template_file = 'my_template.html'
rendered_file = template(template_file, name='Bob', city='London')
print(rendered_file)