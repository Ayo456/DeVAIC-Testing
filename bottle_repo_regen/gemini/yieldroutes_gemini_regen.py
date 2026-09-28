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

# regen 2
from collections.abc import Iterable
from typing import Any, Callable, Generator


def yieldroutes(func: Any) -> Generator[Callable, None, None]:
    """Recursively yields underlying route callback functions from a route handler,

    nested route structure, or standalone callable.
    """
    if func is None:
        return



    nested_candidates = []


    if hasattr(func, "routes") and isinstance(func.routes, Iterable):
        nested_candidates.extend(func.routes)
    if hasattr(func, "app"):
        nested_candidates.append(func.app)
    if hasattr(func, "endpoint"):
        nested_candidates.append(func.endpoint)


    if hasattr(func, "__wrapped__"):
        nested_candidates.append(func.__wrapped__)


    for attr in ("sub_routes", "handlers", "children"):
        if hasattr(func, attr):
            val = getattr(func, attr)
            if isinstance(val, Iterable):
                nested_candidates.extend(val)
            else:
                nested_candidates.append(val)


    if nested_candidates:
        for candidate in nested_candidates:
            yield from yieldroutes(candidate)
    elif callable(func):
        yield func

# regen 3
from collections.abc import Callable, Iterable
from typing import Any, Generator


def yieldroutes(func: Any) -> Generator[Callable[..., Any], None, None]:
    """Recursively yields underlying route callback functions from a handler,

    router, or wrapped callable.
    """
    if func is None:
        return


    nested_candidates = None
    for attr in ("routes", "children", "endpoints", "handlers"):
        val = getattr(func, attr, None)
        if isinstance(val, Iterable) and not isinstance(val, (str, bytes)):
            nested_candidates = val
            break

    if nested_candidates is not None:
        found_any = False
        for route in nested_candidates:

            target = getattr(
                route,
                "endpoint",
                getattr(route, "app", getattr(route, "handler", route)),
            )
            yield from yieldroutes(target)
            found_any = True
        if found_any:
            return


    if hasattr(func, "__wrapped__") and callable(func.__wrapped__):
        yield from yieldroutes(func.__wrapped__)
        return


    if callable(func):
        yield func