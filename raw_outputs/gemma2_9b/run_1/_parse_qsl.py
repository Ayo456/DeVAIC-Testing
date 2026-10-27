```python
def _parse_qsl(qs: str) -> list[tuple[str, str]]:
  return [(name.replace('+', ' ').decode('ascii'), value.replace('+', ' ').decode('ascii')) for name, value in (segment.split('=', 1) for segment in qs.split('&') if segment) ]
```