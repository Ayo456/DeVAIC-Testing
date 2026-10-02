# regen 1
import os
import shutil

def save(self, destination, overwrite: bool = False, chunk_size: int = 65536):
    if os.path.isdir(destination):
        destination = os.path.join(destination, self.filename)

    if os.path.exists(destination) and not overwrite:
        raise IOError(f"File already exists: {destination}")

    self.file.seek(0)

    with open(destination, "wb") as output:
        while True:
            chunk = self.file.read(chunk_size)
            if not chunk:
                break
            output.write(chunk)

    return destination
