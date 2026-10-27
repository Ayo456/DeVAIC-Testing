import urllib.parse

def _parse_qsl(qs: str):
    result = []
    for segment in qs.split('&'):
        if not segment:
            continue
        if '=' in segment:
            name, value = segment.split('=', 1)
        else:
            name, value = (segment, '')
        name = urllib.parse.unquote(name.replace('+', ' '))
        value = urllib.parse.unquote(value.replace('+', ' '))
        result.append((name, value))
    return result