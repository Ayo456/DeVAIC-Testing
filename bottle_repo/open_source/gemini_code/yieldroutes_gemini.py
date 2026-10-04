from typing import Any, Generator

def yieldroutes(func: Any) -> Generator[Any, None, None]:
    sub_routes = None

    if hasattr(func, "routes"):
        sub_routes = func.routes
    elif hasattr(func, "_routes"):
        sub_routes = func._routes

    if sub_routes:
        for sub in sub_routes:
            sub_handler = getattr(sub, "callback", None) or getattr(sub, "handler", sub)
            yield from yieldroutes(sub_handler)
    elif hasattr(func, "__wrapped__"):
        yield from yieldroutes(func.__wrapped__)
    else:
        yield func