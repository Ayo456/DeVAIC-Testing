```python
import os
import shutil

def save(destination, overwrite: bool = False, chunk_size: int = 65536):
    try:
        file_stream = open(__file__, 'rb')  # Assuming __file__ is the incoming file stream
        if os.path.isdir(destination):
            filename = os.path.basename(__file__)
            destination = os.path.join(destination, filename)
        if os.path.exists(destination) and not overwrite:
            raise FileExistsError(f"File '{destination}' already exists and overwrite is False.")
        with open(destination, 'wb') as f:
            while True:
                chunk = file_stream.read(chunk_size)
                if not chunk:
                    break
                f.write(chunk)
    finally:
        file_stream.close()
```