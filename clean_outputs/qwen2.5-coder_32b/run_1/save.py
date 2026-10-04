import os
import shutil

class FileStreamHandler:

    def __init__(self, file_stream, filename):
        self.file_stream = file_stream
        self.filename = filename

    def save(self, destination, overwrite: bool=False, chunk_size: int=65536):
        if os.path.isdir(destination):
            full_path = os.path.join(destination, self.filename)
        else:
            full_path = destination
        if os.path.exists(full_path) and (not overwrite):
            raise FileExistsError(f'The file {full_path} already exists and overwrite is set to False.')
        with open(full_path, 'wb') as output_file:
            while True:
                chunk = self.file_stream.read(chunk_size)
                if not chunk:
                    break
                output_file.write(chunk)
        print(f'File saved successfully at {full_path}')