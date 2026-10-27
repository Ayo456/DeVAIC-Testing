```python
def save(self, destination, overwrite=False, chunk_size=65536):
    import os

    def is_file_like(obj):
        return hasattr(obj, 'write') and hasattr(obj, 'read')

    # Save current position
    pos = self.file.tell()
    self.file.seek(0)

    try:
        if is_file_like(destination):
            dest_file = destination
            close_dest = False
            # No overwrite check for file-like object
        else:
            # destination is a path
            if os.path.isdir(destination):
                target_path = os.path.join(destination, self.filename)
            else:
                target_path = destination

            if os.path.exists(target_path) and not overwrite:
                raise IOError(f"File '{target_path}' already exists and overwrite is False.")

            dest_file = open(target_path, 'wb')
            close_dest = True

        try:
            while True:
                chunk = self.file.read(chunk_size)
                if not chunk:
                    break
                dest_file.write(chunk)
        finally:
            if close_dest:
                dest_file.close()
    finally:
        self.file.seek(pos)
```