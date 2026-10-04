```python
def _file_iter_range(fp, chunk_size=65536):
  """Reads from an open file-like stream in binary chunks.

  Args:
    fp: An open file-like object in binary read mode.
    chunk_size: The size of each chunk to read (in bytes). Defaults to 65536.

  Yields:
    Binary chunks of data from the file.
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
     - `fp`: The open file-like object to read from.
     - `chunk_size`: The size of each chunk (default is 65536 bytes).

2. **Infinite Loop:**
   - `while True:` creates an infinite loop that continues until a `break` statement is encountered.

3. **Reading Chunks:**
   - `chunk = fp.read(chunk_size)` reads a chunk of data from the file `fp` with a maximum size of `chunk_size`.

4. **Check for End of File:**
   - `if not chunk:` checks if the `chunk` variable is empty. If it is, it means the end of the file has been reached.

5. **Break Loop:**
   - `break` exits the infinite loop if no more data is available.

6. **Yield Chunk:**
   - `yield chunk` yields the read chunk of data. This pauses the function execution and returns the chunk to the caller. The next time the generator is called, it resumes from where it left off.

**How to Use:**

```python
with open("my_file.bin", "rb") as f:
  for chunk in _file_iter_range(f):
    # Process each chunk here
    print(f"Processing chunk of size {len(chunk)} bytes")
```



Let me know if you have any other questions.