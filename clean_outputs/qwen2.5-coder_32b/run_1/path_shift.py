def path_shift(script_name: str, path_info: str, shift: int=1) -> tuple:
    script_segments = script_name.rstrip('/').split('/')
    path_segments = path_info.lstrip('/').split('/')
    if script_segments == ['']:
        script_segments = []
    if path_segments == ['']:
        path_segments = []
    num_segments_to_move = shift if shift >= 0 else -shift
    if shift > 0:
        if num_segments_to_move > len(path_segments):
            num_segments_to_move = len(path_segments)
        script_segments.extend(path_segments[:num_segments_to_move])
        path_segments = path_segments[num_segments_to_move:]
    elif shift < 0:
        if num_segments_to_move > len(script_segments):
            num_segments_to_move = len(script_segments)
        path_segments = script_segments[-num_segments_to_move:] + path_segments
        script_segments = script_segments[:-num_segments_to_move]
    new_script_name = '/'.join(script_segments) + ('/' if script_name.endswith('/') else '')
    new_path_info = '/'.join(path_segments) if path_segments else '/' if path_info.startswith('/') else ''
    return (new_script_name, new_path_info)
print(path_shift('/app', '/user/profile', 1))
print(path_shift('/app/user', '/profile', -1))