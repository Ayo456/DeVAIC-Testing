import os
import shutil
from typing import BinaryIO, Union


class FileUpload:
    def __init__(self, file: BinaryIO, filename: str):
        self.file = file
        self.filename = filename

    def save(
        self,
        destination: Union[str, os.PathLike],
        overwrite: bool = False,
        chunk_size: int = 65536,
    ) -> str:
        dest_path = str(destination)

        if os.path.isdir(dest_path):
            dest_path = os.path.join(dest_path, os.path.basename(self.filename))

        if not overwrite and os.path.exists(dest_path):
            raise FileExistsError(f"File already exists: {dest_path}")

        try:
            self.file.seek(0)
        except (AttributeError, OSError):
            pass

        with open(dest_path, "wb") as f_out:
            while True:
                chunk = self.file.read(chunk_size)
                if not chunk:
                    break
                f_out.write(chunk)

        return dest_path