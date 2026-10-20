import os
import shutil

def save(destination, overwrite: bool=False, chunk_size: int=65536):
    import sys
    file_stream = sys.stdin.buffer
    if os.path.isdir(destination):
        default_filename = 'output'
        destination = os.path.join(destination, default_filename)
    if os.path.exists(destination) and (not overwrite):
        raise FileExistsError(f"File '{destination}' already exists and overwrite is False.")
    with open(destination, 'wb') as f:
        while True:
            chunk = file_stream.read(chunk_size)
            if not chunk:
                break
            f.write(chunk)