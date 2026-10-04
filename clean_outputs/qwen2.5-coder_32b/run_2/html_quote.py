import html

def html_quote(string: str) -> str:
    if string is None or string == '':
        return '""'
    escaped_string = html.escape(string, quote=False)
    escaped_string = escaped_string.replace('"', '&quot;')
    return f'"{escaped_string}"'
print(html_quote('Hello, "world"!'))
print(html_quote('<div>Test</div>'))
print(html_quote(None))
print(html_quote(''))