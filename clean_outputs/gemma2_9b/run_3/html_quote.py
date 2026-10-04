def html_quote(string: str) -> str:
    if string is None or string == '':
        return ''
    return f'''"{string.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')}"'''