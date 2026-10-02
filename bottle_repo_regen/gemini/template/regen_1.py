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
