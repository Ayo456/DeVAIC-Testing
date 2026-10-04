def path_shift(script_name: str, path_info: str, shift: int=1) -> tuple:
    script_segments = script_name.rstrip('/').split('/')
    path_segments = path_info.lstrip('/').split('/')
    if shift > 0:
        shift = min(shift, len(path_segments))
        script_segments.extend(path_segments[:shift])
        path_segments = path_segments[shift:]
    elif shift < 0:
        shift = -min(-shift, len(script_segments))
        path_segments = script_segments[shift:] + path_segments
        script_segments = script_segments[:shift]
    new_script_name = '/'.join(script_segments) + '/'
    new_path_info = '/' + '/'.join(path_segments) if path_segments else '/'
    return (new_script_name, new_path_info)