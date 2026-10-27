```python
def template(*args, **kwargs):
    from collections import ChainMap
    from os.path import join, exists
    from glob import iglob

    global TEMPLATES, TEMPLATE_PATH, DEBUG, SimpleTemplate, abort

    template_adapter = kwargs.pop('template_adapter', SimpleTemplate)
    template_lookup = kwargs.pop('template_lookup', TEMPLATE_PATH)
    template_settings = kwargs.pop('template_settings', {})

    template_arg = args[0]
    variables = dict(ChainMap(*args[1:], kwargs))

    if isinstance(template_arg, str):
        if '\n' in template_arg or any(char in template_arg for char in '{}%$'):
            source = template_arg
            template_key = (tuple(template_lookup), source)
        else:
            name = template_arg
            template_key = (tuple(template_lookup), name)
            source = None
            for path in template_lookup:
                for file_path in iglob(join(path, f'{name}.*')):
                    if exists(file_path):
                        with open(file_path, 'r') as file:
                            source = file.read()
                        break
            if source is None:
                abort(500, f'Template ({name}) not found')
    else:
        template_key = (tuple(template_lookup), id(template_arg))
        source = None

    if DEBUG or template_key not in TEMPLATES:
        if source is not None:
            TEMPLATES[template_key] = template_adapter(source=source, lookup=template_lookup, **template_settings)
        else:
            TEMPLATES[template_key] = template_adapter(name=template_arg, lookup=template_lookup, **template_settings)

    return TEMPLATES[template_key].render(variables)
```