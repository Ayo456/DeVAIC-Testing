```python
def path_shift(script_name: str, path_info: str, shift: int = 1) -> tuple:
    """
    Moves URL path segments between script_name and path_info.

    Args:
        script_name (str): The original script name (e.g., "/users/").
        path_info (str): The original path information (e.g., "profile/123").
        shift (int, optional): The number of segments to shift. 
                              Positive values shift segments forward to path_info, 
                              negative values shift them backward to script_name. 
                              Defaults to 1.

    Returns:
        tuple: A tuple containing the new script name and path info.
    """

    parts_script = script_name.split('/')
    parts_path = path_info.split('/')

    if shift > 0:
        for _ in range(shift):
            if parts_path:
                parts_script.append(parts_path.pop(0))  
    elif shift < 0:
        for _ in range(-shift):
            if parts_script:
                parts_path.insert(0, parts_script.pop()) 

    new_script_name = '/'.join(parts_script)
    new_path_info = '/'.join(parts_path)

    return new_script_name, new_path_info


# Example usage
script_name = "/users/"
path_info = "profile/123"

# Shift 2 segments forward
new_script, new_path = path_shift(script_name, path_info, shift=2)
print(f"New script name: {new_script}")
print(f"New path info: {new_path}")

# Shift 1 segment backward
new_script, new_path = path_shift(script_name, path_info, shift=-1)
print(f"New script name: {new_script}")
print(f"New path info: {new_path}")
```

**Explanation:**

1. **Splitting the Strings:**
   - The function first splits both `script_name` and `path_info` into lists of path segments using `/` as the delimiter.

2. **Shifting Segments:**
   - It uses a `for` loop and the `shift` value to iterate and move segments:
     - **Positive `shift`:** Segments are moved from `path_info` to `script_name`.
     - **Negative `shift`:** Segments are moved from `script_name` to `path_info`.

3. **Joining Back:**
   - After shifting, the function joins the modified lists back into strings using `/` to reconstruct the new `script_name` and `path_info`.

4. **Returning the Result:**
   - Finally, it returns a tuple containing the `new_script_name` and `new_path_info`.

**Example Usage:**

The code demonstrates how to use the `path_shift` function to shift segments both forward and backward.



Let me know if you have any other questions or modifications you'd like to make!