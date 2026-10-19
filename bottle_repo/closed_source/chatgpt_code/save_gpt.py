import shutil
from pathlib import Path


def save(self, destination, overwrite: bool = False, chunk_size: int = 65536):
    destination = Path(destination)

    if destination.is_dir():
        destination = destination / self.filename

    if destination.exists() and not overwrite:
        raise FileExistsError(f"File already exists: {destination}")

    destination.parent.mkdir(parents=True, exist_ok=True)

    with destination.open("wb") as target:
        shutil.copyfileobj(self.file, target, length=chunk_size)

    return str(destination)