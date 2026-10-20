```python
def html_quote(string: str) -> str:
  return '"' + string.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;') + '"' if string else ""
```