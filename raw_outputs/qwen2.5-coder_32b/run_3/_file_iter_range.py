Certainly! Below is the implementation of the `_file_iter_range` generator function. This function reads from an open file-like stream in binary chunks of the specified `chunk_size` and yields each chunk until the end of the file is reached.

```python
def _file_iter_range(fp, chunk_size=65536):
    """
    Generator function to read from an open file-like stream in binary chunks.

    Parameters:
    - fp: file-like object, the file stream to read from.
    - chunk_size: int, the size of each chunk to read in bytes (default is 65536).

    Yields:
    - bytes: each chunk of data read from the file.
    """
    while True:
        chunk = fp.read(chunk_size)
        if not chunk:
            break
        yield chunk
```

### Explanation:
- **Parameters**:
  - `fp`: This is the file-like object (e.g., a file opened in binary mode using `open(filename, 'rb')`).
  - `chunk_size`: This is the size of each chunk to read from the file. The default value is 65536 bytes (64 KB).

- **Logic**:
  - The function enters an infinite loop (`while True`).
  - It reads a chunk of data from the file using `fp.read(chunk_size)`.
  - If the chunk is empty (`if not chunk`), it means the end of the file has been reached, and the loop breaks.
  - Otherwise, the chunk is yielded, and the loop continues to read the next chunk.

### Usage Example:
Here is an example of how you might use this generator function:

```python
# Open a file in binary mode
with open('example.bin', 'rb') as file:
    # Iterate over the file in chunks of 65536 bytes
    for chunk in _file_iter_range(file, chunk_size=65536):
        # Process each chunk
        print(f"Read chunk of size: {len(chunk)} bytes")
```

In this example, the file `example.bin` is opened in binary mode, and the generator function is used to read and process the file in chunks of 65536 bytes.