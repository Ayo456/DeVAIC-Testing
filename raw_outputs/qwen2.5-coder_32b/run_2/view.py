Certainly! Below is the implementation of the `view` decorator function as described:

```python
def template(tpl_name, **tplvars):
    # This is a placeholder function to simulate template rendering.
    # In a real application, this would render the template with the given variables.
    return f"Template: {tpl_name} rendered with {tplvars}"

def view(tpl_name, **defaults):
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            
            if isinstance(result, dict):
                # Merge defaults with the returned dictionary
                tplvars = {**defaults, **result}
            elif result is None:
                # Use only defaults if the result is None
                tplvars = defaults
            else:
                # Return the result unmodified if it's not a dictionary or None
                return result
            
            # Render the template with the merged variables
            return template(tpl_name, **tplvars)
        
        return wrapper
    return decorator

# Example usage:
@view('example_template.html', title='Default Title')
def my_route_handler():
    return {'content': 'Hello, World!'}

# This should output: "Template: example_template.html rendered with {'title': 'Default Title', 'content': 'Hello, World!'}"
print(my_route_handler())

@view('example_template.html', title='Default Title')
def my_route_handler_none():
    return None

# This should output: "Template: example_template.html rendered with {'title': 'Default Title'}"
print(my_route_handler_none())

@view('example_template.html', title='Default Title')
def my_route_handler_string():
    return "This is a string response."

# This should output: "This is a string response."
print(my_route_handler_string())
```

### Explanation:
1. **`template` Function**: This is a placeholder function to simulate template rendering. In a real application, you would use a template engine like Jinja2 to render the template with the given variables.
2. **`view` Decorator**: This decorator takes a template name and default template variables as arguments.
3. **`decorator` Function**: This inner function takes the original function (route handler callback) as an argument.
4. **`wrapper` Function**: This function wraps the original function, calls it, and processes its result.
   - If the result is a dictionary, it merges it with the default variables.
   - If the result is `None`, it uses only the default variables.
   - If the result is any other data type, it returns the result unmodified.
5. **Rendering**: The `template` function is called with the merged variables to simulate rendering the template.

You can replace the `template` function with your actual template rendering logic.