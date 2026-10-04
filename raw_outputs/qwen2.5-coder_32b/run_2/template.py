To create a `template` function that can handle template names, file paths, or raw template strings, and render them using provided arguments, we can use the `jinja2` library. This library is widely used for templating in Python and provides a powerful way to render templates.

First, you need to install the `jinja2` library if you haven't already:

```sh
pip install jinja2
```

Now, let's write the `template` function:

```python
import os
from jinja2 import Environment, FileSystemLoader, Template

def template(tpl, *args, **kwargs):
    env = Environment()
    
    if os.path.isfile(tpl):
        # If tpl is a file path, load the template from the file
        with open(tpl, 'r') as file:
            template_str = file.read()
        template = Template(template_str)
    elif os.path.isdir(tpl):
        # If tpl is a directory, set it as the template search path
        env = Environment(loader=FileSystemLoader(tpl))
        template_name = kwargs.pop('template_name', 'default.html')
        template = env.get_template(template_name)
    else:
        # Otherwise, treat tpl as a raw template string
        template = Template(tpl)
    
    # Render the template with the provided arguments
    return template.render(*args, **kwargs)

# Example usage:
# Assuming you have a template file named 'example.html' in the current directory:
# result = template('example.html', name='World')
# print(result)

# Or using a raw template string:
# result = template('Hello, {{ name }}!', name='World')
# print(result)
```

### Explanation:

1. **Environment Setup**: We create a `jinja2.Environment` object. This environment can be configured to load templates from files, directories, or strings.

2. **File Check**: We check if `tpl` is a file path using `os.path.isfile(tpl)`. If it is, we read the file and create a `Template` object from its contents.

3. **Directory Check**: If `tpl` is a directory, we use `FileSystemLoader` to set the directory as the search path for templates. We then get the template using `env.get_template(template_name)`. The `template_name` is provided via the `kwargs` and defaults to `'default.html'`.

4. **Raw Template String**: If `tpl` is neither a file nor a directory, we treat it as a raw template string and create a `Template` object directly.

5. **Rendering**: Finally, we render the template using the provided positional and keyword arguments and return the rendered string.

This function is flexible and can handle different types of template sources while allowing you to pass arguments to the template for rendering.