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
