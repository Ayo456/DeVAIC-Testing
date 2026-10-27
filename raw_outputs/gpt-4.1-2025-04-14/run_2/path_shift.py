```python
def path_shift(script_name: str, path_info: str, shift: int = 1):
    def split_path(p):
        return [s for s in p.strip('/').split('/') if s] if p.strip('/') else []
    def join_path(segments):
        return '/' + '/'.join(segments) if segments else '/'
    orig_path_info_trailing_slash = path_info.endswith('/') and split_path(path_info)
    script_segments = split_path(script_name)
    path_segments = split_path(path_info)
    if shift == 0:
        return (join_path(script_segments), join_path(path_segments))
    elif shift > 0:
        assert len(path_segments) >= shift, "Not enough segments in PATH_INFO to shift"
        move = path_segments[:shift]
        new_script = script_segments + move
        new_path = path_segments[shift:]
    else:
        n = abs(shift)
        assert len(script_segments) >= n, "Not enough segments in SCRIPT_NAME to shift"
        move = script_segments[-n:]
        new_script = script_segments[:-n]
        new_path = move + path_segments
    new_script_name = join_path(new_script)
    new_path_info = join_path(new_path)
    if orig_path_info_trailing_slash and new_path:
        if new_path_info != '/' and not new_path_info.endswith('/'):
            new_path_info += '/'
    return (new_script_name, new_path_info)
```