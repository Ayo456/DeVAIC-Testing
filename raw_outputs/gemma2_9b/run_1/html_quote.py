```python
def html_quote(string: str) -> str:
  return '"' + string.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#039;').replace('\n', '&#10;').replace('\r', '&#13;').replace('\t', '&#9;') + '"'
```