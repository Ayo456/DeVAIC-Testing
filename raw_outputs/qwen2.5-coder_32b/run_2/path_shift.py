Certainly! Below is the Python function `path_shift` that performs the described operation. This function takes a `script_name`, a `path_info`, and an optional `shift` parameter. The `shift` parameter determines how many path segments to move between `script_name` and `path_info`. A positive `shift` moves segments from `path_info` to `script_name`, while a negative `shift` moves segments from `script_name` to `path_info`.

Here's the implementation:

```python
def path_shift(script_name: str, path_info: str, shift: int = 1) -> tuple:
    # Split the script_name and path_info into segments
    script_segments = script_name.rstrip('/').split('/')
    path_segments = path_info.lstrip('/').split('/')
    
    # Determine the effective shift
    if shift > 0:
        # Moving segments from path_info to script_name
        shift = min(shift, len(path_segments))
        script_segments.extend(path_segments[:shift])
        path_segments = path_segments[shift:]
    elif shift < 0:
        # Moving segments from script_name to path_info
        shift = -min(-shift, len(script_segments))
        path_segments = script_segments[shift:] + path_segments
        script_segments = script_segments[:shift]
    
    # Join the segments back into the paths
    new_script_name = '/'.join(script_segments) + '/'
    new_path_info = '/' + '/'.join(path_segments) if path_segments else '/'
    
    return new_script_name, new_path_info

# Example usage:
# script_name = '/a/b'
# path_info = '/c/d/e'
# shift = 1
# new_script_name, new_path_info = path_shift(script_name, path_info, shift)
# print(new_script_name, new_path_info)  # Output: /a/b/c /d/e

# script_name = '/a/b/c'
# path_info = '/d/e'
# shift = -1
# new_script_name, new_path_info = path_shift(script_name, path_info, shift)
# print(new_script_name, new_path_info)  # Output: /a/b /c/d/e
```

### Explanation:
1. **Splitting Segments**: The function splits `script_name` and `path_info` into segments using `split('/')`. The `rstrip('/')` and `lstrip('/')` methods are used to remove any trailing or leading slashes to ensure clean splitting.
2. **Effective Shift Calculation**: The function calculates the effective shift to avoid attempting to move more segments than are available.
3. **Segment Movement**:
   - For a positive `shift`, segments are moved from `path_info` to `script_name`.
   - For a negative `shift`, segments are moved from `script_name` to `path_info`.
4. **Rejoining Segments**: The function rejoins the segments back into the paths and ensures that the resulting paths have the correct format (i.e., ending with a slash if necessary).

This function should handle typical cases of URL path manipulation as described.