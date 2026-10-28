def path_shift(script_name: str, path_info: str, shift: int=1) -> tuple:

    def split_path(path):
        return [segment for segment in path.strip('/').split('/') if segment]
    script_segments = split_path(script_name)
    path_segments = split_path(path_info)
    if shift > 0:
        assert len(path_segments) >= shift, 'Not enough segments in path_info to shift'
        script_segments.extend(path_segments[:shift])
        path_segments = path_segments[shift:]
    elif shift < 0:
        shift = abs(shift)
        assert len(script_segments) >= shift, 'Not enough segments in script_name to shift'
        path_segments = script_segments[-shift:] + path_segments
        script_segments = script_segments[:-shift]
    new_script_name = '/' + '/'.join(script_segments) + '/'
    new_path_info = '/' + '/'.join(path_segments) + ('/' if path_info.endswith('/') and path_segments else '')
    return (new_script_name, new_path_info)