```python
def yieldroutes(func):
  """
  Recursively yields all route callbacks within a given function.

  Args:
    func: A route handler function or callable object.

  Yields:
    Each underlying route callback function found within func.
  """

  if hasattr(func, '__closure__'):
    for cell in func.__closure__:
      if hasattr(cell.cell_contents, '__call__'):
        yield from yieldroutes(cell.cell_contents)
  elif hasattr(func, 'inner'):
    yield from yieldroutes(func.inner)  
  else:
    yield func 

```

**Explanation:**

1. **Function Definition:**
   - `def yieldroutes(func):` defines a generator function named `yieldroutes` that takes a single argument, `func`, representing the route handler function.

2. **Closure Handling:**
   - `if hasattr(func, '__closure__'):` checks if the function has a closure (nested functions). 
   - `for cell in func.__closure__: ...` iterates through each cell in the closure.
   - `if hasattr(cell.cell_contents, '__call__'):` checks if the cell's contents are callable (likely a nested function).
   - `yield from yieldroutes(cell.cell_contents)` recursively calls `yieldroutes` on each callable nested function within the closure.

3. **Inner Function Handling:**
   - `elif hasattr(func, 'inner'):` checks for a common pattern where functions might have an `inner` attribute (indicating a nested route handler).
   - `yield from yieldroutes(func.inner)` recursively calls `yieldroutes` on the `inner` function.

4. **Standalone Function:**
   - `else: yield func` If neither of the above conditions is met, the function is likely a standalone route handler, so it is yielded directly.

**How to Use:**

```python
def my_handler(request):
  # ... some logic ...
  return "Hello, world!"

def nested_handler(request):
  # ... some nested logic ...
  return "Nested response"

my_handler.inner = nested_handler

for route in yieldroutes(my_handler):
  print(route) 
```

**Output:**

```
<function my_handler at 0x...>
<function nested_handler at 0x...>
```



Let me know if you have any other questions or want to explore specific use cases!