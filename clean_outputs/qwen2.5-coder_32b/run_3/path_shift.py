def path_shift(script_name: str, path_info: str, shift: int=1) -> tuple:
    script_segments = script_name.rstrip('/').split('/')
    path_segments = path_info.lstrip('/').split('/')
    total_segments = len(script_segments) + len(path_segments)
    if total_segments == 0:
        return (script_name, path_info)
    effective_shift = shift % total_segments
    if effective_shift > 0:
        move_segments = path_segments[:effective_shift]
        script_segments.extend(move_segments)
        path_segments = path_segments[effective_shift:]
    elif effective_shift < 0:
        effective_shift = -effective_shift
        move_segments = script_segments[-effective_shift:]
        path_segments = move_segments + path_segments
        script_segments = script_segments[:-effective_shift]
    new_script_name = '/'.join(script_segments) + '/'
    new_path_info = '/' + '/'.join(path_segments)
    return (new_script_name, new_path_info)
script_name = '/a/b'
path_info = '/c/d/e'
shift = 2
new_script_name, new_path_info = path_shift(script_name, path_info, shift)
print(new_script_name)
print(new_path_info)