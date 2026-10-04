Certainly! Below is a Python generator function named `_iter_chunked` that reads and parses a chunked transfer encoding stream using a `read_func` callback. It yields byte segments for each valid chunk and terminates upon encountering a zero-length chunk. If a chunk header exceeds `bufsize` or contains invalid hexadecimal characters, it raises an appropriate exception.

```python
def _iter_chunked(read_func, bufsize: int = 102400):
    def read_line():
        """Read a single line from the read_func, respecting bufsize."""
        line = bytearray()
        while True:
            byte = read_func(1)
            if not byte:
                break
            line.append(byte[0])
            if line.endswith(b'\r\n'):
                break
            if len(line) > bufsize:
                raise ValueError("Chunk header exceeds bufsize")
        return line

    while True:
        # Read the chunk length line
        chunk_length_line = read_line()
        if not chunk_length_line:
            raise ValueError("Unexpected end of stream while reading chunk length")

        # Strip the CRLF and parse the chunk length
        try:
            chunk_length_str = chunk_length_line.decode('ascii').split(';', 1)[0].strip()
            chunk_length = int(chunk_length_str, 16)
        except ValueError:
            raise ValueError(f"Invalid chunk length header: {chunk_length_line}")

        # If the chunk length is zero, we've reached the end of the stream
        if chunk_length == 0:
            # Read and discard any trailing headers
            while read_line().strip():
                pass
            break

        # Read the chunk data
        chunk_data = bytearray()
        while len(chunk_data) < chunk_length:
            data = read_func(chunk_length - len(chunk_data))
            if not data:
                raise ValueError("Unexpected end of stream while reading chunk data")
            chunk_data.extend(data)

        # Read the CRLF that follows the chunk data
        crlf = read_func(2)
        if crlf != b'\r\n':
            raise ValueError("Expected CRLF after chunk data")

        # Yield the chunk data
        yield chunk_data

# Example usage:
# def read_func(size):
#     # This function should read 'size' bytes from the source and return them as bytes.
#     pass

# for chunk in _iter_chunked(read_func):
#     print(chunk)
```

### Explanation:
1. **Reading Lines**: The `read_line` function reads a line from the `read_func` until it encounters `\r\n`. It also ensures that the line does not exceed `bufsize`.
2. **Chunk Length Parsing**: The chunk length is extracted from the line by decoding it to ASCII, splitting off any chunk extensions, and converting the hexadecimal string to an integer.
3. **Zero-Length Chunk**: If the chunk length is zero, the function reads and discards any trailing headers and terminates.
4. **Reading Chunk Data**: The function reads the specified number of bytes for the chunk data and checks for the trailing `\r\n`.
5. **Yielding Chunks**: Valid chunks are yielded one by one.

This function should handle the chunked transfer encoding as specified, raising exceptions for invalid headers or unexpected end-of-stream conditions.