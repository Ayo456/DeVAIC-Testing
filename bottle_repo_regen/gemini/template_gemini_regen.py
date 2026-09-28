# regen 1
from pathlib import Path
import jinja2

def template(tpl, *args, **kwargs):
    """
    Renders a template from a raw string, file path, or template name.
    
    Positional args are exposed as `args` (e.g. {{ args[0] }}),
    and keyword args are directly available in the context.
    """
    path = Path(tpl)
    

    if path.is_file():
        env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(str(path.parent or ".")),
            autoescape=jinja2.select_autoescape()
        )
        template_obj = env.get_template(path.name)
    else:

        env = jinja2.Environment(autoescape=jinja2.select_autoescape())
        template_obj = env.from_string(tpl)
        
    context = {"args": args, **kwargs}
    return template_obj.render(context)

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

# regen 3
from pathlib import Path
from string import Template


def template(tpl: str, *args, **kwargs) -> str:
    """Render a template string, file path, or named template using positional

    (format-style) and keyword substitutions.
    """
    path = Path(tpl)
    if path.is_file():
        content = path.read_text(encoding="utf-8")
    else:
        content = tpl


    if args:
        try:
            return content.format(*args, **kwargs)
        except (KeyError, IndexError, ValueError):
            pass


    try:
        return Template(content).safe_substitute(**kwargs)
    except Exception:
        pass


    try:
        return content.format(**kwargs)
    except Exception:
        return content