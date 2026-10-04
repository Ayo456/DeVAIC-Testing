def path_shift(script_name: str, path_info: str, shift: int=1) -> tuple:
    parts_script = script_name.split('/')
    parts_path = path_info.split('/')
    shift_count = min(abs(shift), len(parts_path))
    if shift > 0:
        parts_script.extend(parts_path[:shift_count])
        parts_path = parts_path[shift_count:]
    else:
        parts_path.extend(parts_script[:shift_count])
        parts_script = parts_script[shift_count:]
    new_script_name = '/'.join(parts_script)
    new_path_info = '/'.join(parts_path)
    return (new_script_name, new_path_info)