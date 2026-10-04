To create a generator function `yieldroutes(func)` that inspects a route handler callback function or callable object, we need to define what "nested routes" or "wrapped child handlers" mean in this context. For simplicity, let's assume that a route handler might contain other route handlers as attributes or in a specific structure (e.g., a list or dictionary).

Here's a possible implementation:

1. If the function has an attribute `__routes__` which is a list or dictionary of route handlers, recursively yield each handler.
2. If the function is a standalone function, yield the function itself.

Let's implement this:

```python
def yieldroutes(func):
    """
    Generator function that yields all route callback functions from a given route handler.
    
    :param func: The route handler function or callable object to inspect.
    """
    if hasattr(func, '__routes__'):
        routes = func.__routes__
        if isinstance(routes, dict):
            routes = routes.values()
        for route in routes:
            yield from yieldroutes(route)
    else:
        yield func

# Example usage:
def route1():
    print("This is route 1")

def route2():
    print("This is route 2")

def route3():
    print("This is route 3")

# Simulating nested routes
class NestedRouteHandler:
    def __init__(self):
        self.__routes__ = {
            'route2': route2,
            'route3': route3
        }

# Simulating a standalone route handler
def standalone_route():
    print("This is a standalone route")

# Simulating a route handler with nested routes
def main_route():
    print("This is the main route")

main_route.__routes__ = NestedRouteHandler().__routes__

# Yielding routes from main_route
for route in yieldroutes(main_route):
    print(route.__name__)
```

In this example:
- `main_route` has nested routes defined in `__routes__`.
- `NestedRouteHandler` is a class that simulates a route handler with nested routes.
- `yieldroutes` will recursively yield `route2` and `route3` when called with `main_route`.

When you run the example, it will print:
```
route2
route3
```

This implementation assumes that the nested routes are stored in the `__routes__` attribute of the function or callable object. If the structure is different, you would need to adjust the logic accordingly.