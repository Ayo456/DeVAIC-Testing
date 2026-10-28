def save(self, destination, overwrite=False, chunk_size=65536):
    if isinstance(destination, str):
        if os.path.isdir(destination):
            destination = os.path.join(destination, self.filename)
            if os.path.exists(destination) and (not overwrite):
                raise IOError
        with open(destination, 'wb') as f:
            self._save_to_file(f, chunk_size)
    elif isinstance(destination, io.IOBase):
        self._save_to_file(destination, chunk_size)
    else:
        raise TypeError('Destination must be a file path, directory path, or open binary file-like object.')
    self.file.seek(0)