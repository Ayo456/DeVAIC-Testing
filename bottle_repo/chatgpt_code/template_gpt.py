from pathlib import Path


def template(tpl, *args, **kwargs):
    path = Path(str(tpl))

    if path.is_file():
        source = path.read_text(encoding="utf-8")
    else:
        source = str(tpl)

    return source.format(*args, **kwargs)