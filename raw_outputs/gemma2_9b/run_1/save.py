```python
import os

def save(destination, overwrite: bool = False, chunk_size: int = 65536):
  """Reads an incoming file stream and writes it to disk.

  Args:
    destination: The path to the destination file or directory.
    overwrite: Whether to overwrite an existing file (default: False).
    chunk_size: The size of each chunk to read and write (default: 65536 bytes).

  Raises:
    FileExistsError: If the destination file already exists and overwrite is False.
  """
  if os.path.isfile(destination):
    if not overwrite:
      raise FileExistsError(f"File '{destination}' already exists. Use overwrite=True to replace it.")

  if os.path.isdir(destination):
    # If destination is a directory, use the default filename
    destination = os.path.join(destination, os.path.basename(destination))

  with open(destination, 'wb') as f:
    while True:
      chunk = stream.read(chunk_size)
      if not chunk:
        break
      f.write(chunk)

```

**Explanation:**

1. **Imports:** Imports the `os` module for file system operations.
2. **Function Definition:**
   - `save(destination, overwrite=False, chunk_size=65536)`: Defines the function named `save` with parameters:
     - `destination`: Path to the file or directory.
     - `overwrite`: Boolean flag to control overwriting existing files (default is False).
     - `chunk_size`: Size of each chunk to read and write (default is 65536 bytes).

3. **File Existence Check:**
   - `if os.path.isfile(destination):`: Checks if `destination` points to an existing file.
     - `if not overwrite:`: If `overwrite` is False and a file exists, raise a `FileExistsError`.

4. **Directory Handling:**
   - `if os.path.isdir(destination):`: If `destination` is a directory:
     - `destination = os.path.join(destination, os.path.basename(destination))`: Constructs the full path to a file within the directory using the default filename.

5. **Writing to File:**
   - `with open(destination, 'wb') as f:`: Opens the destination file in binary write mode (`'wb'`) using a context manager (ensures the file is closed properly).
   - `while True:`: Loops until the end of the input stream is reached.
     - `chunk = stream.read(chunk_size)`: Reads a chunk of data from the input stream.
     - `if not chunk:`: If no more data is available, break the loop.
     - `f.write(chunk)`: Writes the chunk to the destination file.



**Remember:**

- Replace `stream` with the actual file stream object you want to save.
- Ensure you have the necessary permissions to write to the specified destination.