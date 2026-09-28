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

# regen 2
from pathlib import Path
import shutil
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
        """Reads an incoming file stream and writes it to disk at destination.

        :param destination: File or directory path where the stream should be
        saved.
        :param overwrite: If False, raises FileExistsError if the target file
        exists.
        :param chunk_size: Size of chunks to read from the stream in bytes.
        :return: Path object pointing to the written file.
        :raises FileExistsError: If target file exists and overwrite is False.
        :raises IsADirectoryError: If the resolved path points to an existing
        directory.
        """
        dest_path = Path(destination).expanduser().resolve()

        if dest_path.is_dir():
            target_path = dest_path / self.filename
        else:
            target_path = dest_path

        if target_path.exists():
            if target_path.is_dir():
                raise IsADirectoryError(
                    f"Target path '{target_path}' is an existing directory."
                )
            if not overwrite:
                raise FileExistsError(
                    f"File '{target_path}' already exists and overwrite is set to False."
                )

        target_path.parent.mkdir(parents=True, exist_ok=True)

        with open(target_path, "wb") as dest_file:
            while chunk := self.stream.read(chunk_size):
                dest_file.write(chunk)

        return target_path

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