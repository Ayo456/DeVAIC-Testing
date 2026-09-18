def save(self, destination, overwrite=False, chunk_size=2**16):
    if isinstance(destination, basestring):
        if os.path.isdir(destination):
            destination = os.path.join(destination, self.filename)
        if not overwrite and os.path.exists(destination):
            raise IOError('File exists.')
        with open(destination, 'wb') as fp:
            self._copy_file(fp, chunk_size)
    else:
        self._copy_file(destination, chunk_size)
