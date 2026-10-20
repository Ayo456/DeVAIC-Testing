```python
def save(destination, overwrite: bool = False, chunk_size: int = 65536):
    import os
    if os.path.isdir(destination):
        destination = os.path.join(destination, os.path.basename(stream.name))
    if os.path.exists(destination) and not overwrite:
        raise Exception(f"File '{destination}' already exists.")
    with open(destination, 'wb') as f:
        while True:
            chunk = stream.read(chunk_size)
            if not chunk:
                break
            f.write(chunk)
```