# regen 2
from pathlib import Path

def template(tpl, *args, **kwargs):
    path = Path(tpl)

    if path.is_file():
        source = path.read_text(encoding="utf-8")
    else:
        candidates = [
            Path("templates") / tpl,
            Path("templates") / f"{tpl}.tpl",
            Path("templates") / f"{tpl}.html"
        ]

        source = None

        for candidate in candidates:
            if candidate.is_file():
                source = candidate.read_text(encoding="utf-8")
                break

        if source is None:
            source = tpl

    return source.format(*args, **kwargs)
