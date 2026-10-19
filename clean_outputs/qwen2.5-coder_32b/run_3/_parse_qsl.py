import urllib.parse

def _parse_qsl(qs: str) -> list:
    segments = qs.split('&')
    result = []
    for segment in segments:
        if not segment:
            continue
        if '=' in segment:
            name, value = segment.split('=', 1)
        else:
            name, value = (segment, '')
        name = name.replace('+', ' ')
        value = value.replace('+', ' ')
        name = urllib.parse.unquote(name)
        value = urllib.parse.unquote(value)
        result.append((name, value))
    return result
qs = 'name=John+Doe&age=25&city=New+York&country=&'
print(_parse_qsl(qs))