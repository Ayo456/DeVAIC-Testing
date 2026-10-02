# regen 1
from collections.abc import Generator
from typing import Any, Callable


def yieldroutes(func: Any) -> Generator[Callable[..., Any], None, None]:
    """Recursively yields underlying route callback functions from a route handler,

    container, or wrapper.
    """

    nested_attrs = ("routes", "_routes", "handlers", "children")

    found_nested = False
    for attr in nested_attrs:
        children = getattr(func, attr, None)
        if children and isinstance(children, (list, tuple, set)):
            found_nested = True
            for child in children:

                endpoint = getattr(
                    child,
                    "endpoint",
                    getattr(child, "app", getattr(child, "handle", child)),
                )
                yield from yieldroutes(endpoint)


    if not found_nested and hasattr(func, "__wrapped__"):
        yield from yieldroutes(func.__wrapped__)
        return


    if not found_nested and callable(func):
        yield func
