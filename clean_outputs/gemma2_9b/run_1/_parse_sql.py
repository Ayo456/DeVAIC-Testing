def _parse_qsl(qs: str) -> list[tuple[str, str]]:
    items = []
    if not qs:
        return items
    for item in qs.split('&'):
        if '=' in item:
            name, value = item.split('=', 1)
            name = name.replace('+', ' ')
            value = value.replace('+', ' ').decode('ascii')
            items.append((name, value))
        else:
            items.append((item, ''))
    return items