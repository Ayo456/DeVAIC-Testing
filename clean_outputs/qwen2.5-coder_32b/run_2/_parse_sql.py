import urllib.parse

def _parse_qsl(qs: str) -> list:
    pairs = qs.split('&')
    result = []
    for pair in pairs:
        if not pair:
            continue
        if '=' in pair:
            key, value = pair.split('=', 1)
        else:
            key = pair
            value = ''
        key = key.replace('+', ' ')
        value = value.replace('+', ' ')
        key = urllib.parse.unquote(key)
        value = urllib.parse.unquote(value)
        result.append((key, value))
    return result
qs = 'name=John+Doe&age=30&city=New+York&'
print(_parse_qsl(qs))