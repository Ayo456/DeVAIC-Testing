Certainly! Below is a Python generator function named `_file_iter_range` that reads from an open file-like stream `fp` in binary chunks of `chunk_size` bytes and yields each chunk sequentially until the stream is exhausted.

```python
def _file_iter_range(fp, chunk_size=65536):
    """
    Generator function to read from a file-like stream in binary chunks.

    :param fp: An open file-like stream in binary mode.
    :param chunk_size: The size of each chunk to read, default is 65536 bytes.
    :yield: Binary chunks of data from the file-like stream.
    """
    while True:
        chunk = fp.read(chunk_size)
        if not chunk:
            break
        yield chunk
```

### Explanation:
- **Parameters**:
  - `fp`: The file-like stream from which to read. It should be opened in binary mode (e.g., using `open('filename', 'rb')`).
  - `chunk_size`: The size of each chunk to read. The default is set to 65536 bytes (64 KB), which is a common choice for efficient I/O operations.
  
- **Functionality**:
  - The function enters an infinite loop (`while True`) to continuously read chunks from the file-like stream.
  - `fp.read(chunk_size)` reads up to `chunk_size` bytes from the stream.
  - If `chunk` is empty (`if not chunk`), it means the end of the stream has been reached, and the loop breaks.
  - Otherwise, the chunk is yielded to the caller.

### Example Usage:
Here's how you might use this generator function:

```python
# Open a binary file
with open('example.bin', 'rb') as fp:
    # Iterate over the file in chunks
    for chunk in _file_iter_range(fp):
        # Process each chunk
        print(len(chunk))  # For example, print the size of each chunk
```

This function is useful for processing large files in a memory-efficient manner by reading and processing them in smaller chunks.