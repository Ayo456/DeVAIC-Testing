from jinja2 import Environment, FileSystemLoader, Template

def template(tpl, *args, **kwargs):
    try:
        with open(tpl, 'r') as file:
            template_str = file.read()
        env = Environment(loader=FileSystemLoader('.'))
        tmpl = env.from_string(template_str)
    except FileNotFoundError:
        try:
            env = Environment(loader=FileSystemLoader('.'))
            tmpl = env.get_template(tpl)
        except Exception:
            tmpl = Template(tpl)
    context = {}
    if args:
        for i, value in enumerate(args):
            context[f'arg{i}'] = value
    context.update(kwargs)
    return tmpl.render(context)
rendered_text = template('example.html', name='World')
print(rendered_text)
raw_template = '<h1>Hello, {{ name }}!</h1>'
rendered_text = template(raw_template, name='World')
print(rendered_text)