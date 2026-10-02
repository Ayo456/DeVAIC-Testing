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
