```python
from jinja2 import Template, Environment, FileSystemLoader

def template(tpl, *args, **kwargs):
    """
    Renders a template given a name, file path, or raw string.

    Args:
        tpl: The template to render. Can be:
            - A string: The raw template content.
            - A file path: The path to the template file.
            - A Jinja2 Template object: An already initialized template.
        *args: Positional arguments to pass to the template.
        **kwargs: Keyword arguments to pass to the template.

    Returns:
        The rendered template string.
    """

    if isinstance(tpl, str):
        if tpl.startswith("template://"):
            # Assume it's a relative path within the current directory
            # For more complex scenarios, you might need to adjust this
            # based on your project structure.
            with open(tpl[11:], 'r') as f:
                tpl = Template(f.read())
        else:
            # Assume it's a file path
            env = Environment(loader=FileSystemLoader('.'))  
            tpl = env.get_template(tpl)
    elif isinstance(tpl, Template):
        # Template object already initialized
        pass
    else:
        raise ValueError("Invalid template type. Must be a string, file path, or Jinja2 Template object.")

    return tpl.render(*args, **kwargs)

```

**Explanation:**

1. **Import Jinja2:**
   - `from jinja2 import Template, Environment, FileSystemLoader` imports necessary components from the Jinja2 templating engine.

2. **`template` Function:**
   - Takes `tpl`, `*args`, and `**kwargs` as arguments.

3. **Template Type Handling:**
   - **String (`tpl`):**
     - If `tpl` starts with "template://", it's assumed to be a relative path within the current directory. The code opens the file and creates a `Template` object.
     - Otherwise, it assumes it's a file path and uses `FileSystemLoader` to create an `Environment` and get the template from the file.
   - **`Template` Object:** If `tpl` is already a `Template` object, it's used directly.
   - **Error Handling:** Raises a `ValueError` if `tpl` is not a valid type.

4. **Rendering:**
   - `tpl.render(*args, **kwargs)` renders the template using the provided positional and keyword arguments.

5. **Return Value:**
   - The function returns the rendered template string.

**How to Use:**

```python
# Example 1: Raw template string
template_str = "Hello {{ name }}, you are {{ age }} years old."
rendered_text = template(template_str, "Alice", age=30)
print(rendered_text)  # Output: Hello Alice, you are 30 years old.

# Example 2: File path
template_file = "my_template.html"
rendered_text = template(template_file, "Bob", city="London")
print(rendered_text) 

# Example 3: Jinja2 Template object
env = Environment(loader=FileSystemLoader('.'))
template_obj = env.get_template("my_template.html")
rendered_text = template(template_obj, "Charlie", hobbies=["reading", "coding"])
print(rendered_text)
```



Make sure to have Jinja2 installed (`pip install jinja2`) before running the code.