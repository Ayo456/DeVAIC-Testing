```python
def html_quote(string: str) -> str:
    if string is None or string == "":
        return '""'
    escaped = string.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')
    return f'"{escaped}"'
```