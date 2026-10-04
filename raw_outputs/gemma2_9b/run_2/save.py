```python
import os

class FileHandler:
    def save(self, destination, overwrite: bool = False, chunk_size: int = 65536):
        """
        Reads an incoming file stream and writes it to disk at the specified destination.

        Args:
            destination (str): The path to the destination file or directory.
            overwrite (bool, optional): If True, overwrites the existing file if it exists. Defaults to False.
            chunk_size (int, optional): The size of each chunk to read and write. Defaults to 65536 bytes.

        Raises:
            FileExistsError: If the destination file exists and overwrite is False.
        """

        if os.path.isdir(destination):
            # If destination is a directory, use the default filename
            filename = os.path.basename(self.stream.name)
            destination = os.path.join(destination, filename)

        if os.path.exists(destination) and not overwrite:
            raise FileExistsError(f"File '{destination}' already exists. Use overwrite=True to replace it.")

        with open(destination, 'wb') as f:
            while True:
                chunk = self.stream.read(chunk_size)
                if not chunk:
                    break
                f.write(chunk)

```

**Explanation:**

1. **`FileHandler` Class:**
   - We create a simple `FileHandler` class to encapsulate the file saving logic. You can add more methods to this class for other file operations if needed.

2. **`save()` Method:**
   - **Arguments:**
     - `destination (str)`: The path where the file should be saved.
     - `overwrite (bool, optional)`: Determines whether to overwrite an existing file (default: `False`).
     - `chunk_size (int, optional)`:  The size of data read and written in each chunk (default: 65536 bytes).

   - **Directory Handling:**
     - If `destination` is a directory, it gets the filename from the input stream (`self.stream.name`) and constructs the full file path within the directory.

   - **File Existence Check:**
     - If a file already exists at the `destination` and `overwrite` is `False`, a `FileExistsError` is raised to prevent accidental overwriting.

   - **Writing to Disk:**
     - The code opens the `destination` file in binary write mode (`'wb'`).
     - It reads data from the input stream (`self.stream`) in chunks of `chunk_size`.
     - Each chunk is written to the destination file.
     - The loop continues until no more data is available in the input stream (`chunk` becomes empty).

**Important:**

- Replace `self.stream` with the actual file stream object you're reading from.



Let me know if you have any other questions or want to modify this further!