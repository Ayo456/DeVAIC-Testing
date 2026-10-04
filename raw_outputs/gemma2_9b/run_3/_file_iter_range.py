```python
def _file_iter_range(fp, chunk_size=65536):
    """
    Reads from an open file-like stream fp in binary chunks of chunk_size bytes.

    Yields each chunk sequentially until the stream returns no more data.

    Args:
        fp: An open file-like object.
        chunk_size: The size of each chunk in bytes (default: 65536).

    Yields:
        bytes: A chunk of bytes from the file stream.
    """
    while True:
        chunk = fp.read(chunk_size)
        if not chunk:
            return
        yield chunk
```

**Explanation:**

1. **Function Definition:**
   - `def _file_iter_range(fp, chunk_size=65536):` defines a generator function named `_file_iter_range` that takes two arguments:
     - `fp`: The open file-like object to read from.
     - `chunk_size`: The desired size of each chunk (in bytes), defaulting to 65536.

2. **Infinite Loop (`while True`):**
   - The function enters an infinite loop to continuously read chunks until the end of the file is reached.

3. **Reading a Chunk (`fp.read(chunk_size)`):**
   - Inside the loop, `fp.read(chunk_size)` reads a chunk of bytes from the file object `fp`. The `read()` method returns the read data as a bytes object.

4. **Empty Chunk Check (`if not chunk`):**
   - `if not chunk:` checks if the `read()` method returned an empty bytes object. This indicates that the end of the file has been reached.

5. **Return Statement (`return`):**
   - If the chunk is empty, the `return` statement exits the function, signaling the end of the generator.

6. **Yielding the Chunk (`yield chunk`):**
   - If the chunk is not empty, `yield chunk` yields the read chunk to the caller. This pauses the function's execution and returns the chunk. When the caller requests the next chunk, the function resumes from where it left off.

**Usage Example:**

```python
with open("my_file.bin", "rb") as fp:
    for chunk in _file_iter_range(fp):
        # Process each chunk here
        print(len(chunk), "bytes read")
```



Let me know if you have any other questions!