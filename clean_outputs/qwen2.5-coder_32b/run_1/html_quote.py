def html_quote(string: str) -> str:
    if string is None or string == '':
        return '""'
    escaped_string = string.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#x27;')
    return f'"{escaped_string}"'
print(html_quote('Hello, World!'))
print(html_quote('He said, "Hello!"'))
print(html_quote(None))
print(html_quote(''))