To implement the `template` function as described, we can use the Jinja2 templating engine, which is a popular choice for rendering templates in Python. Jinja2 allows us to load templates from files or strings and render them with provided data.

Here's the step-by-step implementation of the `template` function:

1. **Install Jinja2**: If you haven't already, you can install Jinja2 using pip:
   ```bash
   pip install Jinja2
   ```

2. **Implement the `template` function**:
   - First, we need to check if the `tpl` is a file path or a raw template string.
   - We then use Jinja2 to load the template and render it with the provided arguments.

Here is the complete implementation:

```python
import os
from jinja2 import Environment, FileSystemLoader, Template

def template(tpl, *args, **kwargs):
    env = Environment()

    # Check if tpl is a file path
    if os.path.isfile(tpl):
        # Set up the file system loader
        env = Environment(loader=FileSystemLoader(os.path.dirname(tpl)))
        template_name = os.path.basename(tpl)
        tmpl = env.get_template(template_name)
    else:
        # Assume tpl is a raw template string
        tmpl = Template(tpl)

    # Render the template with provided arguments
    return tmpl.render(*args, **kwargs)

# Example usage:
# Assuming you have a file 'example.txt' with content:
# Hello, {{ name }}!
# You can call the function as follows:
# result = template('example.txt', name='World')
# print(result)  # Output: Hello, World!

# Alternatively, using a raw template string:
# result = template('Hello, {{ name }}!', name='World')
# print(result)  # Output: Hello, World!
```

### Explanation:
1. **Environment Setup**:
   - We create a Jinja2 `Environment` object. If `tpl` is a file path, we set up a `FileSystemLoader` to load the template from the file system.

2. **Template Loading**:
   - If `tpl` is a file path, we use `os.path.isfile` to check its existence and then load the template using `env.get_template`.
   - If `tpl` is a raw string, we directly create a `Template` object with the string content.

3. **Rendering**:
   - We render the template using `tmpl.render(*args, **kwargs)`, which allows us to pass both positional and keyword arguments to the template.

This function should work for both file-based templates and raw string templates, providing flexibility in how you specify your templates.