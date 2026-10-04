import os
import shutil
from pathlib import Path

class FileStreamSaver:

    def __init__(self, file_stream, default_filename):
        self.file_stream = file_stream
        self.default_filename = default_filename

    def save(self, destination, overwrite=False, chunk_size=65536):
        destination_path = Path(destination)
        if destination_path.is_dir():
            destination_path = destination_path / self.default_filename
        if destination_path.exists() and (not overwrite):
            raise FileExistsError(f'The file {destination_path} already exists and overwrite is False.')
        with open(destination_path, 'wb') as f:
            while True:
                chunk = self.file_stream.read(chunk_size)
                if not chunk:
                    break
                f.write(chunk)