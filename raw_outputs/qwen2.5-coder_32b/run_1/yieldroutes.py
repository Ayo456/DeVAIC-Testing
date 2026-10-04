To achieve the functionality described, we need to inspect the structure of the provided function or callable object. This involves checking if the function is a standalone function or if it contains nested routes or wrapped child handlers. For simplicity, let's assume that nested routes or wrapped child handlers are stored in a specific attribute (e.g., `__child_routes__`) of the function object.

Here's how you can implement the `yieldroutes` generator function:

1. Check if the function has a `__child_routes__` attribute.
2. If it does, recursively yield each route from the `__child_routes__` list.
3. If it doesn't, yield the function itself.

Here's the implementation:

```python
def yieldroutes(func):
    """
    Recursively yield each underlying route callback from the provided function or callable object.
    
    :param func: The route handler callback function or callable object to inspect.
    """
    # Check if the function has the __child_routes__ attribute
    if hasattr(func, '__child_routes__'):
        # Recursively yield each child route
        for child in func.__child_routes__:
            yield from yieldroutes(child)
    else:
        # Yield the function itself if it has no child routes
        yield func

# Example usage:

def standalone_route():
    return "Standalone route"

def parent_route():
    return "Parent route"

# Simulate nested routes by adding a __child_routes__ attribute
parent_route.__child_routes__ = [
    standalone_route,
    lambda: "Child route 1",
    lambda: "Child route 2"
]

# Using the generator function
for route in yieldroutes(parent_route):
    print(route.__name__ if hasattr(route, '__name__') else route.__class__.__name__)
```

In this example:
- `standalone_route` is a standalone function.
- `parent_route` is a function that has nested routes stored in the `__child_routes__` attribute.
- The `yieldroutes` function will yield `standalone_route`, `lambda: "Child route 1"`, and `lambda: "Child route 2"` when called with `parent_route`.

This implementation assumes that the `__child_routes__` attribute is a list of callable objects. If your actual use case differs, you may need to adjust the attribute name or the way you access nested routes.