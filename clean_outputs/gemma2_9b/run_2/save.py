def save(self, destination, overwrite=False, chunk_size=65536):
    if isinstance(destination, str):
        if os.path.isdir(destination):
            destination = os.path.join(destination, self.filename)
            if os.path.exists(destination) and (not overwrite):
                raise IOError('File already exists')
        elif os.path.exists(destination) and (not overwrite):
            raise IOError('File already exists')
    elif not isinstance(destination, io.IOBase):
        raise TypeError('Destination must be a file path, directory path, or open file-like object')
    with self.file as f:
        if isinstance(destination, io.IOBase):
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                destination.write(chunk)
        else:
            with open(destination, 'wb') as f_dest:
                while True:
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break
                    f_dest.write(chunk)
    self.file.seek(0)