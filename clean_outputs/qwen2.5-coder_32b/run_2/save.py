import os
import shutil

class FileStreamSaver:

    def __init__(self, file_stream, default_filename):
        self.file_stream = file_stream
        self.default_filename = default_filename

    def save(self, destination, overwrite: bool=False, chunk_size: int=65536):
        if os.path.isdir(destination):
            final_destination = os.path.join(destination, self.default_filename)
        else:
            final_destination = destination
        if os.path.exists(final_destination) and (not overwrite):
            raise FileExistsError(f'The file {final_destination} already exists and overwrite is set to False.')
        with open(final_destination, 'wb') as outfile:
            while True:
                data = self.file_stream.read(chunk_size)
                if not data:
                    break
                outfile.write(data)