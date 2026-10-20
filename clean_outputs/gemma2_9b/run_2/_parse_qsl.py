def _parse_qsl(qs: str) -> list[tuple[str, str]]:
    return [(k.decode('ascii'), v.decode('ascii').replace('+', ' ')) for k, v in [p.split('=', 1) for p in qs.split('&') if p]]