```python
def _iter_chunked(read_func, bufsize: int = 102400) -> bytes:
    """
    Reads and parses a chunked transfer encoding stream using a read_func callback.

    Args:
        read_func: A function that takes an integer argument (buffer size) and returns bytes read from the stream.
        bufsize: Maximum buffer size for reading chunk headers and data (default 102400 bytes).

    Yields:
        bytes: Chunks of data as read from the stream.

    Raises:
        ValueError: If a chunk header exceeds bufsize or contains invalid hexadecimal characters.
        StopIteration: When a zero-length chunk is encountered.
    """
    while True:
        chunk_header = read_func(bufsize).decode('ascii').strip()  
        if not chunk_header:
            break  # End of stream

        try:
            chunk_size = int(chunk_header, 16)
        except ValueError:
            raise ValueError(f"Invalid chunk size: {chunk_header}")

        if chunk_size == 0:
            break  # End of chunked stream

        chunk_data = read_func(chunk_size)
        yield chunk_data

        # Read and discard the trailing newline from the chunk header
        read_func(2)  



```

**Explanation:**

1. **Initialization:**
   - The function takes a `read_func` callback (assumed to read from a stream) and an optional `bufsize` parameter (defaulting to 102400 bytes).
   - It enters a `while True` loop to continuously read chunks until a zero-length chunk is encountered or the stream ends.

2. **Chunk Header Reading:**
   - `read_func(bufsize)` reads a chunk of data from the stream using the provided `read_func` with the specified buffer size.
   - The read data is decoded as ASCII and stripped of leading/trailing whitespace.

3. **Chunk Size Parsing:**
   - `int(chunk_header, 16)` attempts to convert the chunk header (expected to be hexadecimal) into an integer.
   - A `ValueError` is raised if the conversion fails, indicating an invalid hexadecimal chunk size.

4. **Zero-Length Chunk Handling:**
   - If `chunk_size` is 0, the loop breaks, signaling the end of the chunked transfer encoding stream.

5. **Chunk Data Reading:**
   - `read_func(chunk_size)` reads the actual chunk data from the stream based on the parsed `chunk_size`.

6. **Yielding Chunks:**
   - The `yield chunk_data` statement yields the read chunk data to the caller. Generators pause execution at `yield`, allowing processing of each chunk individually.

7. **Trailing Newline Discarding:**
   - `read_func(2)` reads and discards the trailing newline character (`\n`) from the chunk header, preparing for the next iteration.

8. **Loop Continuation:**
   - The `while True` loop continues until a zero-length chunk is encountered or the stream ends.



Let me know if you have any other questions or want to explore specific use cases for this generator function.