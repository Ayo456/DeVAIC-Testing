```python
def view(tpl_name, **defaults):
    """
    Decorator for route handler callbacks.

    Merges callback return values with defaults and renders a template.

    Args:
        tpl_name (str): The name of the template to render.
        **defaults: Keyword arguments to be used as default template variables.

    Returns:
        Callable: The decorated route handler callback function.
    """

    def decorator(callback):
        def wrapper(*args, **kwargs):
            result = callback(*args, **kwargs)

            if isinstance(result, dict):
                # Merge callback return with defaults
                result.update(defaults)
                return template(tpl_name, **result)  
            elif result is None:
                # Render template with only defaults
                return template(tpl_name, **defaults)
            else:
                # Return unmodified result
                return result
        return wrapper
    return decorator
```

**Explanation:**

1. **Decorator Structure:**
   - The `view` function itself is a decorator that takes `tpl_name` and `**defaults` as arguments.
   - It returns another function, `decorator`, which is the actual decorator.

2. **`decorator` Function:**
   - This function takes the `callback` function to be decorated as an argument.
   - It defines a nested function `wrapper` which will replace the original `callback` function.

3. **`wrapper` Function:**
   - This function handles the execution of the decorated callback.
   - It calls the original `callback` with the provided arguments (`*args`, `**kwargs`).
   - It then checks the type of the result returned by the `callback`:
     - **`dict`:**  Merges the result with the `defaults` using `update()` and renders the template using `tpl_name` and the merged dictionary.
     - **`None`:** Renders the template using only `defaults`.
     - **Other Types:** Returns the result unmodified.

4. **Return Values:**
   - The `decorator` function returns the `wrapper` function. This means that when you decorate a function with `@view`, you are essentially replacing it with the `wrapper` function.

**Example Usage:**

```python
@view('my_template.html', title='My Website', message='Hello!')
def my_callback(name):
    return {'name': name}

# When my_callback is called with 'Alice', it will render 'my_template.html' with:
# title='My Website'
# message='Hello!'
# name='Alice'
```



Let me know if you have any other questions or would like to explore specific aspects in more detail!