Certainly! Below is a Python generator function named `_file_iter_range` that reads from an open file-like stream `fp` in binary chunks of `chunk_size` bytes and yields each chunk sequentially until the stream is exhausted.

```python
def _file_iter_range(fp, chunk_size=65536):
    """
    Generator function to read from a file-like stream in binary chunks.

    Parameters:
    fp (file-like object): The file-like stream to read from.
    chunk_size (int): The size of each chunk to read, default is 65536 bytes.

    Yields:
    bytes: The next chunk of data from the file-like stream.
    """
    while True:
        chunk = fp.read(chunk_size)
        if not chunk:
            break
        yield chunk
```

### Explanation:
- **Parameters**:
  - `fp`: This is the file-like stream from which data is to be read. It should support the `read` method.
  - `chunk_size`: This is the number of bytes to read in each chunk. The default value is 65536 bytes.
  
- **Yielding Chunks**:
  - The function enters an infinite loop (`while True`) and reads a chunk of data from the file-like stream using `fp.read(chunk_size)`.
  - If the `read` method returns an empty bytes object (`b''`), it indicates that there is no more data to read, and the loop breaks.
  - Otherwise, the chunk is yielded to the caller.

### Example Usage:
Here is an example of how you might use this generator function to read a file in chunks:

```python
# Open a file in binary mode
with open('example.bin', 'rb') as fp:
    for chunk in _file_iter_range(fp, chunk_size=1024):
        # Process each chunk
        print(chunk)
```

In this example, the file `example.bin` is opened in binary mode, and the `_file_iter_range` generator function is used to read and print the file in 1024-byte chunks.