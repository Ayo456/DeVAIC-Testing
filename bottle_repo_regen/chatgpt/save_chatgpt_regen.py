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

# regen 3
from pathlib import Path

def save(self, destination, overwrite: bool = False, chunk_size: int = 65536):
    destination = Path(destination)

    if destination.is_dir():
        destination = destination / self.filename

    if destination.exists() and not overwrite:
        raise FileExistsError(f"File already exists: {destination}")

    destination.parent.mkdir(parents=True, exist_ok=True)

    with open(destination, "wb") as output:
        while True:
            chunk = self.file.read(chunk_size)

            if not chunk:
                break

            output.write(chunk)

    return destination