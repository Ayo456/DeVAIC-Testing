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

# regen 3
def template(tpl, *args, **kwargs):
    adapter = kwargs.pop("template_adapter", SimpleTemplate)
    lookup = kwargs.pop("template_lookup", TEMPLATE_PATH)
    settings = kwargs.pop("template_settings", {})

    if tpl not in TEMPLATES or DEBUG:
        if isinstance(tpl, adapter):
            TEMPLATES[tpl] = tpl
        elif "\n" in tpl or "{" in tpl or "%" in tpl or "$" in tpl:
            TEMPLATES[tpl] = adapter(source=tpl, lookup=lookup, **settings)
        else:
            TEMPLATES[tpl] = adapter(name=tpl, lookup=lookup, **settings)

    for arg in args:
        if isinstance(arg, dict):
            kwargs.update(arg)

    return TEMPLATES[tpl].render(**kwargs)