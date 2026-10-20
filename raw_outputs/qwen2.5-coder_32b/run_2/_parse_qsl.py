```python
def _parse_qsl(qs: str):
    import urllib.parse
    return urllib.parse.parse_qsl(qs, keep_blank_values=True)
```