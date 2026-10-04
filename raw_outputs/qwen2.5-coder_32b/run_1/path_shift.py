Certainly! The function `path_shift` will take three parameters: `script_name`, `path_info`, and an optional `shift` parameter which defaults to 1. The function will move the specified number of URL path segments between `script_name` and `path_info` based on the sign of the `shift` parameter. A positive `shift` will move segments from `path_info` to `script_name`, while a negative `shift` will move segments from `script_name` to `path_info`.

Here's the implementation:

```python
def path_shift(script_name: str, path_info: str, shift: int = 1) -> tuple:
    # Split script_name and path_info into segments
    script_segments = script_name.rstrip('/').split('/')
    path_segments = path_info.lstrip('/').split('/')
    
    # Handle the case where script_name or path_info is empty
    if script_segments == ['']:
        script_segments = []
    if path_segments == ['']:
        path_segments = []
    
    # Calculate the number of segments to move
    num_segments_to_move = shift if shift >= 0 else -shift
    
    # Perform the shift
    if shift > 0:
        # Move segments from path_info to script_name
        if num_segments_to_move > len(path_segments):
            num_segments_to_move = len(path_segments)
        script_segments.extend(path_segments[:num_segments_to_move])
        path_segments = path_segments[num_segments_to_move:]
    elif shift < 0:
        # Move segments from script_name to path_info
        if num_segments_to_move > len(script_segments):
            num_segments_to_move = len(script_segments)
        path_segments = script_segments[-num_segments_to_move:] + path_segments
        script_segments = script_segments[:-num_segments_to_move]
    
    # Join the segments back into strings
    new_script_name = '/'.join(script_segments) + ('/' if script_name.endswith('/') else '')
    new_path_info = '/'.join(path_segments) if path_segments else ('/' if path_info.startswith('/') else '')
    
    return new_script_name, new_path_info

# Example usage:
print(path_shift("/app", "/user/profile", 1))  # Output: ('/app/user', '/profile')
print(path_shift("/app/user", "/profile", -1)) # Output: ('/app', '/user/profile')
```

### Explanation:
1. **Splitting Segments**: The function splits `script_name` and `path_info` into lists of path segments, removing any trailing or leading slashes.
2. **Handling Edge Cases**: It handles cases where `script_name` or `path_info` might be empty.
3. **Calculating Segments to Move**: The number of segments to move is determined by the absolute value of `shift`.
4. **Performing the Shift**:
   - If `shift` is positive, segments are moved from `path_info` to `script_name`.
   - If `shift` is negative, segments are moved from `script_name` to `path_info`.
5. **Reconstructing the Paths**: The segments are joined back into strings, preserving any trailing slashes from the original inputs.

This function should handle various edge cases and provide the expected behavior for moving path segments between `script_name` and `path_info`.