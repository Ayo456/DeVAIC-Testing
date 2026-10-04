```python
def path_shift(script_name: str, path_info: str, shift: int = 1) -> tuple:
    """
    Moves URL path segments between path_info and script_name.

    Args:
      script_name: The current script name (e.g., "my_app").
      path_info: The current path info (e.g., "/users/123").
      shift: The number of segments to shift. Positive values move segments 
             from path_info to script_name, negative values move them the 
             opposite direction.

    Returns:
      A tuple containing the new script_name and new path_info after the shift.
    """
    parts_script = script_name.split("/")
    parts_path = path_info.split("/")

    shift_count = min(abs(shift), len(parts_path))

    if shift > 0:
      # Moving segments from path_info to script_name
      parts_script.extend(parts_path[:shift_count])
      parts_path = parts_path[shift_count:]
    else:
      # Moving segments from script_name to path_info
      parts_path.extend(parts_script[:shift_count])
      parts_script = parts_script[shift_count:]

    new_script_name = "/".join(parts_script)
    new_path_info = "/".join(parts_path)

    return new_script_name, new_path_info
```

**Explanation:**

1. **Splitting:** The function first splits both `script_name` and `path_info` into lists of path segments using the `/` delimiter.
2. **Shifting:** 
   - It calculates the `shift_count` to determine how many segments to move based on the `shift` value and the length of `path_info`.
   - If `shift` is positive, it moves segments from `path_info` to `script_name`.
   - If `shift` is negative, it moves segments from `script_name` to `path_info`.
3. **Reconstructing:** After shifting, it joins the modified lists back into strings using `/` as the separator, creating the `new_script_name` and `new_path_info`.
4. **Returning:** The function returns a tuple containing the `new_script_name` and `new_path_info`.

**Example Usage:**

```python
script_name = "my_app/users"
path_info = "/123/profile"

# Move 2 segments from path_info to script_name
new_script_name, new_path_info = path_shift(script_name, path_info, shift=2)

print(f"New script name: {new_script_name}")  # Output: my_app/users/123/profile
print(f"New path info: {new_path_info}")   # Output: 
```



