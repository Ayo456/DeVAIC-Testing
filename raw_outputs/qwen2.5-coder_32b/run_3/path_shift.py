Certainly! Below is a Python function `path_shift` that performs the described operation of moving URL path segments between `script_name` and `path_info` based on the provided `shift` value.

```python
def path_shift(script_name: str, path_info: str, shift: int = 1) -> tuple:
    # Split the script_name and path_info into segments
    script_segments = script_name.rstrip('/').split('/')
    path_segments = path_info.lstrip('/').split('/')
    
    # Calculate the effective shift
    total_segments = len(script_segments) + len(path_segments)
    if total_segments == 0:
        return (script_name, path_info)
    
    effective_shift = shift % total_segments
    
    # Perform the shift
    if effective_shift > 0:
        # Move segments from path_info to script_name
        move_segments = path_segments[:effective_shift]
        script_segments.extend(move_segments)
        path_segments = path_segments[effective_shift:]
    elif effective_shift < 0:
        # Move segments from script_name to path_info
        effective_shift = -effective_shift
        move_segments = script_segments[-effective_shift:]
        path_segments = move_segments + path_segments
        script_segments = script_segments[:-effective_shift]
    
    # Reconstruct the script_name and path_info
    new_script_name = '/'.join(script_segments) + '/'
    new_path_info = '/' + '/'.join(path_segments)
    
    return (new_script_name, new_path_info)

# Example usage:
script_name = "/a/b"
path_info = "/c/d/e"
shift = 2
new_script_name, new_path_info = path_shift(script_name, path_info, shift)
print(new_script_name)  # Output: "/a/b/c/d/"
print(new_path_info)    # Output: "/e"
```

### Explanation:
1. **Splitting Segments**: The `script_name` and `path_info` are split into lists of path segments.
2. **Effective Shift Calculation**: The effective shift is calculated using the modulo operation to handle cases where the shift value is greater than the total number of segments.
3. **Shifting Segments**:
   - If `effective_shift` is positive, segments are moved from `path_info` to `script_name`.
   - If `effective_shift` is negative, segments are moved from `script_name` to `path_info`.
4. **Reconstruction**: The modified segments are joined back into strings to form the new `script_name` and `path_info`.

This function ensures that the path segments are correctly shifted and handles edge cases such as empty paths or shifts larger than the number of segments.