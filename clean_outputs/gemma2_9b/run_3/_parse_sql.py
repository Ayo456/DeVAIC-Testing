def _parse_qsl(qs: str) -> list[tuple[str, str]]:
    items = []
    for part in qs.split('&'):
        if not part:
            continue
        name, *value = part.split('=', 1)
        value = value[0] if value else ''
        name = name.replace('+', ' ')
        value = value.replace('+', ' ').decode('ascii')
        items.append((name, value))
    return items