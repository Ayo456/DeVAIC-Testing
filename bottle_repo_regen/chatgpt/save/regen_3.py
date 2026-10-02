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
