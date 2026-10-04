import os

class FileHandler:

    def save(self, destination, overwrite: bool=False, chunk_size: int=65536):
        if os.path.isdir(destination):
            filename = os.path.basename(self.stream.name)
            destination = os.path.join(destination, filename)
        if os.path.exists(destination) and (not overwrite):
            raise FileExistsError(f"File '{destination}' already exists. Use overwrite=True to replace it.")
        with open(destination, 'wb') as f:
            while True:
                chunk = self.stream.read(chunk_size)
                if not chunk:
                    break
                f.write(chunk)