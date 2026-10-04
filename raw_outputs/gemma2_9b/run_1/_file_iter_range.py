```python
def _file_iter_range(fp, chunk_size=65536):
  """Reads from an open file-like stream fp in binary chunks of chunk_size bytes.

  Yields each chunk sequentially until the stream returns no more data.

  Args:
    fp: An open file-like stream in binary mode.
    chunk_size: The size of each chunk in bytes. Defaults to 65536.

  Yields:
    bytes: A chunk of data read from the file.
  """
  while True:
    chunk = fp.read(chunk_size)
    if not chunk:
      break
    yield chunk 
```

**Explanation:**

1. **Function Definition:**
   - `def _file_iter_range(fp, chunk_size=65536):` defines the generator function named `_file_iter_range` that takes two arguments:
     - `fp`: The open file-like stream object.
     - `chunk_size`: The size of each chunk (defaults to 65536 bytes).

2. **Loop for Reading Chunks:**
   - `while True:` creates an infinite loop that continues until `break` is encountered.
   - `chunk = fp.read(chunk_size)` reads a chunk of data from the file `fp` with the specified `chunk_size`. If the end of the file is reached, `read()` returns an empty string.

3. **Yielding Chunks:**
   - `if not chunk:` checks if `chunk` is empty (meaning the end of the file was reached).
   - `break` exits the loop if no more data is available.
   - `yield chunk` yields the read `chunk` to the caller. The `yield` keyword makes this function a generator.

**How to Use It:**

```python
with open("my_file.bin", "rb") as f:
  for chunk in _file_iter_range(f, 4096):  # Read in chunks of 4096 bytes
    # Process the chunk here (e.g., write to another file, analyze it, etc.)
```



Let me know if you have any more questions.