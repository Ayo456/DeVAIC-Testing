def _parse_qsl(qs: str) -> list[tuple[str, str]]:
    items = []
    for item in qs.split('&'):
        if item:
            parts = item.split('=', 1)
            name = parts[0].replace('+', ' ').decode('ascii')
            value = parts[1] if len(parts) > 1 else None
            value = value.replace('+', ' ').decode('ascii') if value else None
            items.append((name, value))
    return items