```python
def template(*args, **kwargs):
    from os.path import join
    from hashlib import sha1
    from functools import reduce
    from operator import or_

    global TEMPLATES, TEMPLATE_PATH, DEBUG, SimpleTemplate, abort

    template_adapter = kwargs.pop('template_adapter', SimpleTemplate)
    template_lookup = kwargs.pop('template_lookup', TEMPLATE_PATH)
    template_settings = kwargs.pop('template_settings', {})

    template_arg = args[0]
    variables = reduce(or_, (dict(arg) for arg in args[1:]), kwargs)

    if isinstance(template_arg, str):
        if '\n' in template_arg or any(char in template_arg for char in '{}%$'):
            source = template_arg
            template_key = (tuple(template_lookup), source)
        else:
            name = template_arg
            template_key = (tuple(template_lookup), name)
    else:
        source = template_arg
        template_key = (tuple(template_lookup), id(source))

    if DEBUG or template_key not in TEMPLATES:
        if isinstance(template_arg, str) and '\n' not in template_arg and all(char not in template_arg for char in '{}%$'):
            for path in template_lookup:
                try:
                    with open(join(path, template_arg)) as f:
                        source = f.read()
                        break
                except FileNotFoundError:
                    continue
            else:
                abort(500, f'Template ({template_arg}) not found')
            template = template_adapter(source=source, lookup=template_lookup, **template_settings)
        else:
            template = template_adapter(source=source, lookup=template_lookup, **template_settings) if isinstance(template_arg, str) else template_arg
            if hasattr(template, 'prepare'):
                template.prepare(**template_settings)
        TEMPLATES[template_key] = template
    else:
        template = TEMPLATES[template_key]

    return template.render(variables)
```