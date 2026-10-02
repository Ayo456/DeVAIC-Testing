# regen 3
import os
import shutil
from pathlib import Path
from typing import BinaryIO, Optional, Union

class FileReceiver:
    def __init__(self, stream: BinaryIO, filename: Optional[str] = None):
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
            default_name = self.filename or getattr(self.stream, "name", None)
            if not default_name:
                raise ValueError(
                    "Destination is a directory, but no filename was provided or detected on the stream."
                )
            target_file = dest_path / Path(default_name).name
        else:
            target_file = dest_path

        if target_file.exists() and not overwrite:
            raise FileExistsError(
                f"The target file already exists and overwrite is False: {target_file}"
            )

        target_file.parent.mkdir(parents=True, exist_ok=True)

        with open(target_file, "wb") as f_out:
            while chunk := self.stream.read(chunk_size):
                f_out.write(chunk)

        return target_file
