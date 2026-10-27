```python
def save(self, destination, overwrite=False, chunk_size=65536):
    import os

    def is_file_like(obj):
        return hasattr(obj, 'write') and hasattr(obj, 'read')

    # Save current position
    try:
        pos = self.file.tell()
    except Exception:
        pos = None

    try:
        if is_file_like(destination):
            out_file = destination
            close_out = False
            # Do not check for overwrite if file-like
        else:
            # destination is a path
            if os.path.isdir(destination):
                target_path = os.path.join(destination, self.filename)
            else:
                target_path = destination
            if os.path.exists(target_path) and not overwrite:
                raise IOError(f"File '{target_path}' already exists and overwrite is False.")
            out_file = open(target_path, 'wb')
            close_out = True

        # Save current file position and rewind to start
        if pos is not None:
            self.file.seek(0)
        while True:
            chunk = self.file.read(chunk_size)
            if not chunk:
                break
            out_file.write(chunk)
        out_file.flush()
    finally:
        # Restore file position
        if pos is not None:
            self.file.seek(pos)
        if 'close_out' in locals() and close_out:
            out_file.close()
```