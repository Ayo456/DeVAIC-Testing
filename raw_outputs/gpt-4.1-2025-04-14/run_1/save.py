```python
def save(self, destination, overwrite=False, chunk_size=65536):
    import os

    file_obj = None
    should_close = False

    # Save current position to restore later
    try:
        current_pos = self.file.tell()
    except Exception:
        current_pos = None

    try:
        # Determine if destination is a file-like object
        if hasattr(destination, 'write') and hasattr(destination, 'fileno'):
            file_obj = destination
        elif hasattr(destination, 'write') and not isinstance(destination, (str, bytes, os.PathLike)):
            file_obj = destination
        else:
            # destination is a path (file or directory)
            dest_path = os.fspath(destination)
            if os.path.isdir(dest_path):
                dest_file_path = os.path.join(dest_path, self.filename)
            else:
                dest_file_path = dest_path

            if os.path.exists(dest_file_path) and not overwrite:
                raise IOError(f"File '{dest_file_path}' already exists and overwrite is False.")

            file_obj = open(dest_file_path, 'wb')
            should_close = True

        # Save file position and rewind to start
        if current_pos is not None:
            self.file.seek(0)

        # Copy in chunks
        while True:
            chunk = self.file.read(chunk_size)
            if not chunk:
                break
            file_obj.write(chunk)
        file_obj.flush()
    finally:
        # Restore file position
        if current_pos is not None:
            self.file.seek(current_pos)
        if should_close and file_obj is not None:
            file_obj.close()
```