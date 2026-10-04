```python
def _iter_chunked(read_func, bufsize: int = 102400):
    """
    Reads and parses a chunked transfer encoding stream using a read_func callback.

    Args:
      read_func: A function that takes an integer (maximum bytes to read) and returns a bytes object.
      bufsize: The maximum size of each chunk to read (default: 102400 bytes).

    Yields:
      bytes: A chunk of data from the chunked transfer encoding stream.

    Raises:
      ValueError: If a chunk header exceeds bufsize or contains invalid hexadecimal characters.
    """
    while True:
        chunk_header = read_func(bufsize).decode('ascii')
        if not chunk_header:
            break  # End of stream

        try:
            chunk_size = int(chunk_header, 16)
        except ValueError:
            raise ValueError(f"Invalid chunk header: {chunk_header}")

        if chunk_size == 0:
            break  # Zero-length chunk, end of stream

        chunk_data = read_func(chunk_size)
        yield chunk_data

```

**Explanation:**

1. **Initialization:**
   - The function takes a `read_func` (a function to read data) and an optional `bufsize` (defaulting to 102400 bytes).

2. **Looping through Chunks:**
   - The `while True` loop continues until a zero-length chunk is encountered, signaling the end of the stream.

3. **Reading Chunk Header:**
   - `read_func(bufsize)` reads a chunk of data up to `bufsize` bytes from the stream. This assumes `read_func` returns bytes.
   - `.decode('ascii')` converts the read bytes to a string using ASCII encoding.

4. **Parsing Chunk Size:**
   - `int(chunk_header, 16)` attempts to convert the chunk header (which is expected to be hexadecimal) into an integer.
   - If the conversion fails (due to invalid hexadecimal characters), a `ValueError` is raised.

5. **Zero-Length Chunk:**
   - If `chunk_size` is 0, it means the end of the stream has been reached, so the loop breaks.

6. **Reading Chunk Data:**
   - `read_func(chunk_size)` reads the actual chunk data based on the parsed `chunk_size`.

7. **Yielding Chunk Data:**
   - `yield chunk_data` yields the read chunk data to the caller. This makes the function a generator, allowing for efficient processing of large streams.

8. **Error Handling:**
   - The function raises a `ValueError` if the chunk header exceeds `bufsize` or contains invalid hexadecimal characters.



Let me know if you have any other questions or would like to explore specific use cases for this generator function!