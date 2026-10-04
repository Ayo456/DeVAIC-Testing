import html

def html_quote(string: str) -> str:
    if string is None or string == '':
        return '""'
    escaped_string = html.escape(string)
    return f'"{escaped_string}"'
print(html_quote(None))
print(html_quote(''))
print(html_quote('hello'))
print(html_quote('<script>'))