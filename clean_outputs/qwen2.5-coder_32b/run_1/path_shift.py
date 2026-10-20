def path_shift(script_name: str, path_info: str, shift: int=1) -> tuple:
    script_parts = script_name.rstrip('/').split('/')
    path_parts = path_info.lstrip('/').split('/')
    if shift > 0:
        shift = min(shift, len(path_parts))
        script_parts.extend(path_parts[:shift])
        path_parts = path_parts[shift:]
    elif shift < 0:
        shift = -min(-shift, len(script_parts))
        path_parts = script_parts[shift:] + path_parts
        script_parts = script_parts[:shift]
    new_script_name = '/'.join(script_parts) + '/'
    new_path_info = '/' + '/'.join(path_parts)
    return (new_script_name, new_path_info)