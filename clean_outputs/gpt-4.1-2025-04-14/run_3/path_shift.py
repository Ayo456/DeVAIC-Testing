def path_shift(script_name: str, path_info: str, shift: int=1):

    def split_path(p):
        p = p.strip('/')
        return p.split('/') if p else []

    def join_path(segments):
        return '/' + '/'.join(segments) if segments else '/'
    orig_path_info_trailing_slash = path_info.endswith('/') and path_info.strip('/') != ''
    script_segments = split_path(script_name)
    info_segments = split_path(path_info)
    if shift > 0:
        assert len(info_segments) >= shift, 'Not enough segments in PATH_INFO to shift'
        move = info_segments[:shift]
        script_segments += move
        info_segments = info_segments[shift:]
    elif shift < 0:
        n = abs(shift)
        assert len(script_segments) >= n, 'Not enough segments in SCRIPT_NAME to shift'
        move = script_segments[-n:]
        script_segments = script_segments[:-n]
        info_segments = move + info_segments
    new_script_name = join_path(script_segments)
    new_path_info = join_path(info_segments)
    if orig_path_info_trailing_slash and len(info_segments) > 0:
        if not new_path_info.endswith('/'):
            new_path_info += '/'
    return (new_script_name, new_path_info)