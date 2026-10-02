# regen 1
import os
import shutil
from pathlib import Path
from typing import BinaryIO, Union


class UploadedFile:
    def __init__(self, stream: BinaryIO, filename: str = "upload.bin"):
        self.stream = stream
        self.filename = filename

    def save(
        self,
        destination: Union[str, Path],
        overwrite: bool = False,
        chunk_size: int = 65536,
    ) -> Path:
        dest_path = Path(destination)

        if dest_path.is_dir():
            target_path = dest_path / self.filename
        else:
            target_path = dest_path

        if target_path.exists() and not overwrite:
            raise FileExistsError(
                f"File '{target_path}' already exists and overwrite=False."
            )

        target_path.parent.mkdir(parents=True, exist_ok=True)

        mode = "wb" if overwrite else "xb"
        with open(target_path, mode) as out_file:
            while chunk := self.stream.read(chunk_size):
                out_file.write(chunk)

        return target_path
