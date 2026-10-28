import os
import string

def template(tpl: str, *args, **kwargs) -> str:
    if os.path.isfile(tpl):
        with open(tpl, 'r', encoding='utf-8') as f:
            template_str = f.read()
    else:
        template_str = tpl
    formatter = string.Formatter()
    return formatter.vformat(template_str, args, kwargs)