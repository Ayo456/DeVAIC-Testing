```python
def save(self, destination, overwrite=False, chunk_size=65536):
    import os
    original_position = self.file.tell()
    try:
        if hasattr(destination, 'write'):
            target = destination
        else:
            if os.path.isdir(destination):
                destination = os.path.join(destination, self.filename)
            if os.path.exists(destination) and not overwrite:
                raise IOError(f"File {destination} already exists and overwrite is False.")
            target = open(destination, 'wb')
        
        while True:
            chunk = self.file.read(chunk_size)
            if not chunk:
                break
            target.write(chunk)
    finally:
        self.file.seek(original_position)
        if not hasattr(destination, 'write'):
            target.close()
```