To achieve this, we can use the `jinja2` library, which is a powerful and flexible template engine for Python. It allows us to load templates from files, strings, and render them with provided context (positional and keyword arguments).

First, you'll need to install the `jinja2` library if you haven't already. You can do this using pip:

```sh
pip install jinja2
```

Now, let's write the `template` function:

```python
from jinja2 import Environment, FileSystemLoader, Template

def template(tpl, *args, **kwargs):
    # Check if tpl is a file path
    try:
        with open(tpl, 'r') as file:
            template_str = file.read()
        env = Environment(loader=FileSystemLoader('.'))
        tmpl = env.from_string(template_str)
    except FileNotFoundError:
        # If tpl is not a file path, assume it's a template name or raw string
        try:
            # Try to load as a template name from the current directory
            env = Environment(loader=FileSystemLoader('.'))
            tmpl = env.get_template(tpl)
        except Exception:
            # If it fails, treat it as a raw template string
            tmpl = Template(tpl)
    
    # Render the template with the provided arguments
    context = {}
    if args:
        # If positional arguments are provided, assume they are named arguments
        # and convert them to a dictionary
        for i, value in enumerate(args):
            context[f'arg{i}'] = value
    context.update(kwargs)
    
    return tmpl.render(context)

# Example usage:
# Assuming you have a template file named 'example.html' with content:
# <h1>Hello, {{ name }}!</h1>
# And you want to render it with the name 'World'

# Render from a file
rendered_text = template('example.html', name='World')
print(rendered_text)

# Render from a raw string
raw_template = "<h1>Hello, {{ name }}!</h1>"
rendered_text = template(raw_template, name='World')
print(rendered_text)
```

### Explanation:
1. **Loading the Template:**
   - The function first tries to open `tpl` as a file path. If successful, it reads the content of the file and creates a `Template` object.
   - If a `FileNotFoundError` is raised, it assumes `tpl` might be a template name or a raw template string.
   - It then tries to load `tpl` as a template name from the current directory using `FileSystemLoader`.
   - If that fails, it treats `tpl` as a raw template string and creates a `Template` object directly.

2. **Rendering the Template:**
   - The function constructs a context dictionary from the provided positional and keyword arguments.
   - Positional arguments are assumed to be named arguments and are converted to a dictionary with keys `arg0`, `arg1`, etc.
   - The `kwargs` are then added to this context.
   - Finally, the template is rendered with the constructed context and the resulting string is returned.

This function should cover the basic requirements of locating or initializing a template, rendering it with provided arguments, and returning the rendered text string.