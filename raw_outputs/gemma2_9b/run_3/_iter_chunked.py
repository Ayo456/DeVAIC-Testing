```python
def _iter_chunked(read_func, bufsize: int = 102400) -> iter[bytes]:
    """
    Reads and parses a chunked transfer encoding stream using a read_func callback.

    Args:
        read_func: A function that takes no arguments and returns a bytes object
            representing the next chunk of data to read.
        bufsize: The maximum size of a single chunk header.

    Yields:
        Bytes representing each valid chunk of data.

    Raises:
        ValueError: If a chunk header exceeds bufsize or contains invalid hexadecimal characters.
    """
    while True:
        chunk_header = read_func()
        if not chunk_header:
            break  # End of stream

        try:
            chunk_size = int(chunk_header.strip(), 16)
        except ValueError:
            raise ValueError("Invalid hexadecimal chunk size in header: {}".format(chunk_header))

        if chunk_size > bufsize:
            raise ValueError("Chunk size exceeds maximum allowed size: {}".format(chunk_size))

        chunk_data = read_func()
        if len(chunk_data) != chunk_size:
            raise ValueError("Chunk data length does not match header size.")

        yield chunk_data

        if chunk_size == 0:
            break  # End of chunked stream



```

**Explanation:**

1. **Function Definition:**
   - `_iter_chunked(read_func, bufsize: int = 102400) -> iter[bytes]`
     - Takes a `read_func` (a function to read chunks) and an optional `bufsize` (defaulting to 102400 bytes) as arguments.
     - Uses `-> iter[bytes]` to specify that it returns an iterator yielding bytes.

2. **Loop for Chunk Processing:**
   - `while True:`: An infinite loop to read and process chunks until the end of the stream is reached.

3. **Reading Chunk Header:**
   - `chunk_header = read_func()`: Calls the `read_func` to read the next chunk header (which is a line).

4. **End of Stream Check:**
   - `if not chunk_header:`: Checks if `read_func()` returned an empty bytes object, indicating the end of the stream. If so, `break` the loop.

5. **Parsing Chunk Size:**
   - `try...except ValueError`: Attempts to parse the `chunk_header` as a hexadecimal integer using `int(chunk_header.strip(), 16)`.
   - If parsing fails (due to invalid hexadecimal characters), a `ValueError` is raised with a helpful message.

6. **Size Validation:**
   - `if chunk_size > bufsize:`: Raises a `ValueError` if the parsed `chunk_size` exceeds the allowed `bufsize`.

7. **Reading Chunk Data:**
   - `chunk_data = read_func()`: Reads the actual data for the chunk.
   - `if len(chunk_data) != chunk_size:`: Checks if the length of the read data matches the header size. If not, raises a `ValueError`.

8. **Yielding Chunk Data:**
   - `yield chunk_data`: Yields the valid `chunk_data` to the caller.

9. **Zero-Length Chunk Check:**
   - `if chunk_size == 0:`: If the `chunk_size` is 0, it indicates the end of the chunked stream. `break` the loop.



**Key Points:**

- **Generator Function:** The use of `yield` makes this a generator function, which efficiently produces chunks one at a time without storing the entire stream in memory.
- **Error Handling:** The code includes `try...except` blocks and `raise ValueError` statements to handle potential errors during chunk header parsing and data reading.
- **`bufsize` Parameter:** Allows you to control the maximum size of a chunk header to prevent memory issues with excessively large headers.