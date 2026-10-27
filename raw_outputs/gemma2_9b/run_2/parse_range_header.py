```python
def parse_range_header(header, maxlen=0):
  if not header or not header.startswith("bytes="):
    return
  for part in header.split("bytes=")[1].split(","):
    if "=" in part:
      continue
    if "-" not in part:
      continue
    start, end = part.split("-")
    if start:
      start = int(start)
      if end:
        end = int(end)
      else:
        end = maxlen
    else:
      end = int(end)
      start = maxlen - end
    if 0 <= start < end <= maxlen:
      yield (start, end)
```