# regen 2
import os

def save(self, destination, overwrite: bool = False, chunk_size: int = 65536):
    destination = os.fspath(destination)

    if os.path.isdir(destination):
        destination = os.path.join(destination, self.filename)

    if os.path.exists(destination) and not overwrite:
        raise FileExistsError(f"File already exists: {destination}")

    with open(destination, "wb") as target:
        while True:
            chunk = self.file.read(chunk_size)

            if not chunk:
                break

            target.write(chunk)

    return destination
