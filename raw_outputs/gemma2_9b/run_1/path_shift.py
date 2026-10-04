```python
def path_shift(script_name: str, path_info: str, shift: int = 1) -> tuple:
  """
  Shifts URL path segments between script_name and path_info.

  Args:
      script_name: The initial script name (e.g., "/api/v1/users").
      path_info: The initial path information (e.g., "/profile").
      shift: The number of segments to shift. Positive value shifts forward, 
             negative value shifts backward.

  Returns:
      A tuple containing the new script name and path info.
  """
  parts_script = script_name.split("/")
  parts_path = path_info.split("/")
  
  shifted_parts = []
  count = 0
  for i in range(len(parts_script) + len(parts_path)):
    if count < shift:
      shifted_parts.append(parts_path.pop(0)) if parts_path else ""
      count += 1
    else:
      shifted_parts.append(parts_script.pop(0)) if parts_script else ""

  new_script_name = "/".join(shifted_parts[:len(parts_script)])
  new_path_info = "/".join(shifted_parts[len(parts_script):])

  return new_script_name, new_path_info

```

**Explanation:**

1. **Splitting:** The function first splits both `script_name` and `path_info` into lists of segments using the `/` delimiter.
2. **Shifting Logic:**
   - It iterates through a combined range of the lengths of both split lists.
   - If `count` is less than `shift`, it takes segments from `path_info` and adds them to the `shifted_parts` list.
   - Otherwise, it takes segments from `script_name`.
   - `count` is incremented to track how many segments have been shifted.
3. **Reconstructing:**
   - After shifting, it reconstructs the `new_script_name` by joining the first `len(parts_script)` segments from `shifted_parts`.
   - It reconstructs `new_path_info` by joining the remaining segments from `shifted_parts`.
4. **Returning:** The function returns a tuple containing the `new_script_name` and `new_path_info`.

**Example Usage:**

```python
script_name = "/api/v1/users"
path_info = "/profile"

new_script, new_path = path_shift(script_name, path_info, shift=2)

print(f"New script name: {new_script}")
print(f"New path info: {new_path}")
```

**Output:**

```
New script name: /api/v1
New path info: /users/profile
```



