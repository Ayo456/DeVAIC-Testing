```python
def html_escape(string: str) -> str:
    escape_map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;',
    }
    return ''.join(escape_map.get(c, c) for c in string)
```