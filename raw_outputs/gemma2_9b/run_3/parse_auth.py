```python
def parse_auth(header: str) -> tuple[str, str] | tuple[str, str]:
  if isinstance(header, str) and header.startswith("Basic "):
    try:
      encoded = header.split(" ")[1]
      decoded = base64.b64decode(encoded).decode("ascii")
      user, password = decoded.split(":")
      return user, password
    except:
      return None
  elif isinstance(header, str):
    parts = header.split(" ", 1)
    if len(parts) == 2:
      return parts[0], parts[1]
    else:
      return None
  else:
    return None 
```