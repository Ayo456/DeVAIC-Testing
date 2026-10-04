def html_quote(string: str) -> str:
    if string is None or string == '':
        return ''
    return '"' + string.replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;') + '"'