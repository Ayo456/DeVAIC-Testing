import os
import shutil

def save(destination, overwrite: bool=False, chunk_size: int=65536):
    if hasattr(destination, 'read'):
        file_stream = destination
        destination = file_stream.name if not os.path.isdir(destination.name) else os.path.join(destination.name, os.path.basename(file_stream.name))
    else:
        file_stream = open(destination, 'rb')
    if os.path.exists(destination) and (not overwrite):
        raise FileExistsError(f"File '{destination}' already exists and overwrite is False.")
    with open(destination, 'wb') as f:
        while True:
            chunk = file_stream.read(chunk_size)
            if not chunk:
                break
            f.write(chunk)
    file_stream.close()