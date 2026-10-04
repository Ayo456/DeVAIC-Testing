```python
import os

class FileSaver:
    def save(self, destination, overwrite: bool = False, chunk_size: int = 65536):
        """
        Reads a file stream and writes it to disk at the specified destination.

        Args:
            destination (str): The path to the destination file or directory.
            overwrite (bool, optional): Whether to overwrite an existing file. Defaults to False.
            chunk_size (int, optional): The size of each chunk to read and write. Defaults to 65536 bytes.

        Raises:
            FileExistsError: If the target file already exists and overwrite is False.
        """

        if os.path.isfile(destination):
            if not overwrite:
                raise FileExistsError(f"File '{destination}' already exists. Use overwrite=True to replace it.")

        if os.path.isdir(destination):
            # If destination is a directory, use the default filename
            destination = os.path.join(destination, os.path.basename(destination))

        with open(destination, 'wb') as f:
            while True:
                chunk = self.stream.read(chunk_size)
                if not chunk:
                    break
                f.write(chunk)

```

**Explanation:**

1. **Import `os`:** Used for file system operations.
2. **`FileSaver` Class:**  This is a simple class to encapsulate the saving functionality. You can instantiate it if you need to reuse the `save` method multiple times with different streams.
3. **`save` Method:**
   - **Arguments:**
     - `destination`: The path where you want to save the file.
     - `overwrite`: A boolean flag indicating whether to overwrite an existing file (default is `False`).
     - `chunk_size`: The size of data chunks to read and write (default is 65536 bytes).
   - **File Existence Check:**
     - Checks if `destination` points to an existing file.
     - If it's a file and `overwrite` is `False`, it raises a `FileExistsError`.
   - **Directory Handling:**
     - If `destination` is a directory, it uses the default filename of the incoming stream and constructs the full file path within the directory.
   - **Writing to Disk:**
     - Opens the destination file in binary write mode (`'wb'`).
     - Reads data from the `stream` in chunks of `chunk_size`.
     - Writes each chunk to the file.
     - Continues until the end of the stream is reached (no more data to read).

**Key Points:**

- **Error Handling:**  The code handles the common scenario of an existing file and prevents accidental overwriting if `overwrite` is `False`.
- **Chunking:** Reading and writing in chunks is efficient for large files as it avoids loading the entire file into memory at once.
- **Flexibility:** The class structure allows you to reuse the `save` method with different file streams.



Let me know if you have any other questions or modifications you'd like to make!