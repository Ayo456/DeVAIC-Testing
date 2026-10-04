To implement the `_iter_chunked` generator function, we need to handle the following steps:

1. Continuously read from the stream using the `read_func` callback.
2. Parse the chunk length from the headers, which are in hexadecimal format.
3. Yield the byte segments for each valid chunk.
4. Stop reading and terminate the generator when a zero-length chunk is encountered.
5. Raise an exception if a chunk header exceeds the specified `bufsize` or contains invalid hexadecimal characters.

Here is the implementation of the `_iter_chunked` generator function:

```python
def _iter_chunked(read_func, bufsize: int = 102400):
    """
    Generator function to read and parse a chunked transfer encoding stream.
    
    :param read_func: A callable that reads from the stream and returns bytes.
    :param bufsize: Maximum size of the chunk header buffer.
    :yield: Byte segments for each valid chunk.
    :raises ValueError: If the chunk header exceeds bufsize or contains invalid hex characters.
    """
    def read_until_newline():
        """Read from the stream until a newline character is encountered."""
        buffer = bytearray()
        while True:
            char = read_func(1)
            if not char:
                break
            buffer.extend(char)
            if buffer.endswith(b'\r\n'):
                return buffer[:-2]  # Remove the CRLF
        raise ValueError("Unexpected end of stream while reading chunk header")

    while True:
        # Read the chunk header (length in hex)
        header = read_until_newline()
        if len(header) > bufsize:
            raise ValueError(f"Chunk header exceeds buffer size of {bufsize} bytes")

        try:
            chunk_length = int(header, 16)
        except ValueError:
            raise ValueError(f"Invalid hexadecimal chunk length: {header}")

        if chunk_length == 0:
            # Read and discard the trailing CRLF after the zero-length chunk
            trailer = read_func(2)
            if trailer != b'\r\n':
                raise ValueError(f"Expected CRLF after zero-length chunk, got: {trailer}")
            break

        # Read the chunk data
        chunk_data = bytearray()
        while len(chunk_data) < chunk_length:
            data = read_func(chunk_length - len(chunk_data))
            if not data:
                raise ValueError("Unexpected end of stream while reading chunk data")
            chunk_data.extend(data)

        # Read and discard the CRLF at the end of the chunk
        crlf = read_func(2)
        if crlf != b'\r\n':
            raise ValueError(f"Expected CRLF at the end of chunk, got: {crlf}")

        yield bytes(chunk_data)

# Example usage:
# def read_func(n):
#     # This should be replaced with actual stream reading logic
#     return b''

# for chunk in _iter_chunked(read_func):
#     print(chunk)
```

### Explanation:
1. **`read_until_newline` Function**: This helper function reads from the stream until it encounters a newline character (`\r\n`), which marks the end of a chunk header. It removes the newline characters before returning the header.

2. **Reading and Parsing Chunk Length**: The chunk length is read and parsed from the header. If the header exceeds `bufsize` or contains invalid hexadecimal characters, a `ValueError` is raised.

3. **Reading Chunk Data**: The function reads the chunk data of the specified length. If the end of the stream is reached before the chunk is fully read, a `ValueError` is raised.

4. **Reading and Discarding CRLF**: After each chunk, the function reads and discards the trailing CRLF (`\r\n`). If the expected CRLF is not found, a `ValueError` is raised.

5. **Termination**: The generator terminates when a zero-length chunk is encountered, and the trailing CRLF is read and discarded.

This function should work correctly for parsing a chunked transfer encoding stream, adhering to the specified requirements.