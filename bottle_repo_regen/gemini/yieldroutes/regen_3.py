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
