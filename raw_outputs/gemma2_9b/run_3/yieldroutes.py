```python
def yield_routes(func):
  """
  Recursively yields all underlying route handlers from a given function.

  Args:
    func: A function or callable object representing a route handler.

  Yields:
    Each underlying route handler function, including nested routes and wrapped child handlers.
  """
  if hasattr(func, '__wrapped__'):
    func = func.__wrapped__  # Unwrap potential decorators

  if isinstance(func, type) or not callable(func):
    yield func
    return

  try:
    # Attempt to inspect function body for nested routes or handlers
    for line in func.__code__.co_code.decode('utf-8').splitlines():
      if line.startswith('route('):
        yield_routes(eval(line.split('route(')[1].rstrip('),').strip()))
  except (AttributeError, SyntaxError, NameError):
    # Handle cases where introspection fails gracefully
    yield func 
```

**Explanation:**

1. **`yield_routes(func)`:**
   - The function takes a single argument `func`, which represents the route handler to inspect.

2. **Unwrapping Decorators:**
   - `if hasattr(func, '__wrapped__'): func = func.__wrapped__`: This line checks if the function has a `__wrapped__` attribute, which indicates that it's a decorated function. If so, it unwraps the decorator to get the original function.

3. **Handling Non-Callable Types:**
   - `if isinstance(func, type) or not callable(func): yield func; return`: This handles cases where `func` is not a callable object (e.g., a class or a non-function type). It directly yields the `func` and exits the function.

4. **Introspection and Recursion:**
   - `try ... except`: The code uses a `try-except` block to handle potential errors during introspection.
   - `for line in func.__code__.co_code.decode('utf-8').splitlines()`: This iterates through each line of the function's bytecode.
   - `if line.startswith('route('):`: This checks if a line starts with `route()`, indicating a potential nested route definition.
   - `yield_routes(eval(line.split('route(')[1].rstrip('),').strip()))`: If a nested route is found, the code evaluates the code inside the `route()` call and recursively calls `yield_routes` to process it.

5. **Handling Errors:**
   - `except (AttributeError, SyntaxError, NameError): yield func`: If any errors occur during introspection (e.g., the function doesn't have bytecode, syntax errors, or undefined names), the function yields the original `func` to avoid crashing.



Let me know if you have any more questions or want to explore specific use cases!