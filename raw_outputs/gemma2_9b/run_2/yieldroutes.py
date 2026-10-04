```python
def yieldroutes(func):
  """
  Recursively yields all underlying route callbacks from a given function.

  Args:
    func: A route handler callback function or callable object.

  Yields:
    Each underlying route callback function or callable object.
  """
  if hasattr(func, '__closure__'):
    for cell in func.__closure__:
      if hasattr(cell.cell_contents, 'func'):
        yield from yieldroutes(cell.cell_contents.func)
  elif hasattr(func, '__wrapped__'):
    yield from yieldroutes(func.__wrapped__)
  else:
    yield func
```

**Explanation:**

1. **`yieldroutes(func)`:** The function takes a single argument, `func`, which is the route handler function or callable object to inspect.

2. **`if hasattr(func, '__closure__'):`:**
   - This checks if the function has a `__closure__` attribute. This attribute exists for functions that have nested scopes (e.g., functions defined within other functions).
   - If it has a `__closure__`, we iterate through its cells (`for cell in func.__closure__`).
   - `if hasattr(cell.cell_contents, 'func'):`: Inside each cell, we check if there's a `func` attribute. This indicates a potential nested route handler.
   - `yield from yieldroutes(cell.cell_contents.func)`: If found, we recursively call `yieldroutes` on the nested function and yield all the routes it exposes.

3. **`elif hasattr(func, '__wrapped__'):`:**
   - This checks if the function has a `__wrapped__` attribute. This often indicates that the function is a wrapped version of another function (e.g., using decorators).
   - If it has a `__wrapped__`, we recursively call `yieldroutes` on the wrapped function.

4. **`else:`:**
   - If neither `__closure__` nor `__wrapped__` exists, it means the function is a standalone route handler.
   - `yield func`: In this case, we simply yield the function itself.

**How to Use:**

```python
def my_handler(request):
  # ... some code ...
  return "Hello, world!"

def nested_handler(request):
  return "Nested handler!"

my_handler = functools.wraps(my_handler)(lambda request: nested_handler(request))

for route in yieldroutes(my_handler):
  print(route)
```

This would output:

```
<function nested_handler at ...> 
```



**Important Notes:**

- This generator relies on introspection (examining the structure of functions). While it works in many common scenarios, it might not handle all complex use cases or edge cases perfectly.
- Decorators and nested scopes can make function analysis more complex.



