import os
import string
from typing import Any, Dict


class SimpleTemplate:
    def __init__(self, source: str):
        self.source = source

    def render(self, *args: Any, **kwargs: Any) -> str:
        context: Dict[str, Any] = {}
        for arg in args:
            if isinstance(arg, dict):
                context.update(arg)
        context.update(kwargs)
        return string.Template(self.source).safe_substitute(context)


TEMPLATES: Dict[str, SimpleTemplate] = {}


def template(tpl: str, *args: Any, **kwargs: Any) -> str:
    if tpl not in TEMPLATES:
        if "\n" not in tpl and (
            os.path.isfile(tpl) or os.path.exists(tpl)
        ):
            with open(tpl, "r", encoding="utf-8") as f:
                source = f.read()
        else:
            source = tpl
        TEMPLATES[tpl] = SimpleTemplate(source)

    return TEMPLATES[tpl].render(*args, **kwargs)