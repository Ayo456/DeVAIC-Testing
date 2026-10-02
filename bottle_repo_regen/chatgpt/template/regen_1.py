# regen 1
from pathlib import Path


def template(tpl, *args, **kwargs) -> str:
    if hasattr(tpl, "render"):
        return str(tpl.render(*args, **kwargs))

    tpl = str(tpl)

    candidates = [
        Path(tpl),
        Path("templates") / tpl,
        Path("templates") / f"{tpl}.tpl"
    ]

    source = None

    for path in candidates:
        if path.is_file():
            source = path.read_text(encoding="utf-8")
            break

    if source is None:
        source = tpl

    return source.format(*args, **kwargs)
