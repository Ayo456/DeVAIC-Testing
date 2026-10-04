import os

def save(destination, overwrite: bool=False, chunk_size: int=65536):
    if os.path.isfile(destination):
        if not overwrite:
            raise FileExistsError(f"File '{destination}' already exists. Use overwrite=True to replace it.")
    if os.path.isdir(destination):
        destination = os.path.join(destination, os.path.basename(destination))
    with open(destination, 'wb') as f:
        while True:
            chunk = stream.read(chunk_size)
            if not chunk:
                break
            f.write(chunk)