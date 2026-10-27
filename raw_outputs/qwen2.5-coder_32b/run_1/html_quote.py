```python
def html_quote(string: str) -> str:
    replacements = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;',
        '\n': '&#10;',
        '\r': '&#13;',
        '\t': '&#9;'
    }
    escaped_string = ''.join(replacements.get(char, char) for char in string)
    return f'"{escaped_string}"'
```