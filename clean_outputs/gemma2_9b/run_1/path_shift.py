def path_shift(script_name: str, path_info: str, shift: int=1) -> tuple:
    parts_script = script_name.split('/')
    parts_path = path_info.split('/')
    shifted_parts = []
    count = 0
    for i in range(len(parts_script) + len(parts_path)):
        if count < shift:
            shifted_parts.append(parts_path.pop(0)) if parts_path else ''
            count += 1
        else:
            shifted_parts.append(parts_script.pop(0)) if parts_script else ''
    new_script_name = '/'.join(shifted_parts[:len(parts_script)])
    new_path_info = '/'.join(shifted_parts[len(parts_script):])
    return (new_script_name, new_path_info)