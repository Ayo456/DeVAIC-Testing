Certainly! Below is a Python class with a method `save` that meets your requirements. This class will handle reading from an incoming file stream and writing it to disk at the specified destination. If the destination is a directory, it will save the file using its default filename. If the target file already exists and `overwrite` is `False`, it will raise an exception.

```python
import os
import shutil

class FileStreamHandler:
    def __init__(self, file_stream, filename):
        self.file_stream = file_stream
        self.filename = filename

    def save(self, destination, overwrite: bool = False, chunk_size: int = 65536):
        # Determine the full path where the file will be saved
        if os.path.isdir(destination):
            full_path = os.path.join(destination, self.filename)
        else:
            full_path = destination

        # Check if the file already exists and overwrite is False
        if os.path.exists(full_path) and not overwrite:
            raise FileExistsError(f"The file {full_path} already exists and overwrite is set to False.")

        # Write the file in chunks
        with open(full_path, 'wb') as output_file:
            while True:
                chunk = self.file_stream.read(chunk_size)
                if not chunk:
                    break
                output_file.write(chunk)

        print(f"File saved successfully at {full_path}")

# Example usage:
# with open('example.txt', 'rb') as file_stream:
#     handler = FileStreamHandler(file_stream, 'example.txt')
#     handler.save('/path/to/destination', overwrite=False)
```

### Explanation:
1. **Initialization**: The `FileStreamHandler` class is initialized with a file stream and a filename.
2. **Save Method**:
   - **Destination Handling**: It checks if the `destination` is a directory. If it is, it constructs the full path by joining the directory with the filename.
   - **File Existence Check**: It checks if the file already exists at the full path. If it does and `overwrite` is `False`, it raises a `FileExistsError`.
   - **Chunked Writing**: It reads the file stream in chunks of the specified `chunk_size` and writes them to the output file. This is useful for handling large files without consuming too much memory.

### Example Usage:
The example usage shows how to use the `FileStreamHandler` class to save a file from a stream to a specified destination. Make sure to replace `'/path/to/destination'` with the actual path where you want to save the file.