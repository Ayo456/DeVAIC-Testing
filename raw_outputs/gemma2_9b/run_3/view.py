```python
def view(tpl_name, **defaults):
    """Decorator for route handler callbacks.

    Args:
        tpl_name: The name of the template to render.
        **defaults: Default template variables.

    Returns:
        A decorated function that renders the template based on the callback's return value.
    """
    def decorator(callback):
        def wrapper(*args, **kwargs):
            result = callback(*args, **kwargs)

            if isinstance(result, dict):
                # Merge defaults with callback results
                result.update(defaults)
                return template(tpl_name, **result)
            elif result is None:
                # Render template with defaults only
                return template(tpl_name, **defaults)
            else:
                # Return unmodified result
                return result
        return wrapper
    return decorator

```

**Explanation:**

1. **`view(tpl_name, **defaults)`:** This is the outer function that takes the template name and default variables as arguments.
2. **`decorator(callback)`:** This inner function takes the route handler callback function as input. It's the function that will be returned by `view` and used to decorate the callback.
3. **`wrapper(*args, **kwargs)`:** This is the function that will actually be executed when the decorated route is called. It takes any positional and keyword arguments passed to the original callback function.
4. **`result = callback(*args, **kwargs)`:** It calls the original callback function and stores its return value in the `result` variable.
5. **`if isinstance(result, dict):`:** This checks if the callback returned a dictionary.
   - If true, it merges the `defaults` with the `result` dictionary using `result.update(defaults)`.
   - Then, it calls the `template` function (assumed to be a function that renders templates) with the `tpl_name` and the merged dictionary as variables.
6. **`elif result is None:`:** This checks if the callback returned `None`.
   - If true, it renders the template using only the `defaults`.
7. **`else:`:** If the callback returned something other than a dictionary or `None` (e.g., a string or response object), it returns the `result` unmodified.

**Usage:**

```python
@view('my_template.html', title='My Website')
def my_handler(request):
    # ... your route handler logic ...
    return {'content': 'Hello, world!', 'user': user_data}

@view('another_template.html')
def another_handler(request):
    # ... your route handler logic ...
    return None  # Render with only defaults
```



Let me know if you have any other questions.