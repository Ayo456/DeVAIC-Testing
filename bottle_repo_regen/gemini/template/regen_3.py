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
