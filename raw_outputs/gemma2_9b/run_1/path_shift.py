```python
def path_shift(script_name: str, path_info: str, shift: int = 1) -> tuple[str, str]:
    script_segments = [s for s in script_name.split('/') if s]
    path_segments = [s for s in path_info.split('/') if s]
    if shift > 0:
        assert len(path_segments) >= shift
        script_segments.extend(path_segments[:shift])
        path_segments = path_segments[shift:]
    elif shift < 0:
        assert len(script_segments) >= abs(shift)
        path_segments.extend(script_segments[-abs(shift):])
        script_segments = script_segments[:-abs(shift)]
    return '/'.join(script_segments) + '/', '/'.join(path_segments) + ('/' if len(path_segments) > 0 else '') 
```