```python
def save(destination, overwrite: bool = False, chunk_size: int = 65536):
    if os.path.isdir(destination):
        destination = os.path.join(destination, input_file.name)
    if os.path.exists(destination) and not overwrite:
        raise FileExistsError(f"File '{destination}' already exists.")
    with open(destination, 'wb') as f:
        while True:
            chunk = input_stream.read(chunk_size)
            if not chunk:
                break
            f.write(chunk)
```