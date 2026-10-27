```python
def html_quote(string: str) -> str:
    escape_map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;',
        '\n': '&#10;',
        '\r': '&#13;',
        '\t': '&#9;',
    }
    return '"' + ''.join(escape_map.get(c, c) for c in string) + '"'
```