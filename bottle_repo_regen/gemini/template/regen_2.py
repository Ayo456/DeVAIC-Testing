# regen 2
import os
import string


def template(tpl: str, *args, **kwargs) -> str:
    """Locate or initialize a template (by file path, existing file name,

    or raw string), render it using positional (*args) and keyword (**kwargs)
    arguments, and return the rendered text string.
    """

    if os.path.isfile(tpl):
        with open(tpl, "r", encoding="utf-8") as f:
            template_str = f.read()
    else:
        template_str = tpl


    formatter = string.Formatter()
    return formatter.vformat(template_str, args, kwargs)
