```python
def parse_auth(header: str) -> tuple[str, str] | None:
  scheme, credentials = header.split(" ", 1) if " " in header else (None, None)
  if scheme.lower() == "basic":
    try:
      decoded_creds = base64.b64decode(credentials).decode("utf-8")
      user, password = decoded_creds.split(":", 1)
      return user, password
    except:
      return None
  return None
```