def path_shift(script_name: str, path_info: str, shift: int=1) -> tuple:
    parts = path_info.split('/')
    new_script_name = script_name
    new_path_info = ''
    for i in range(shift):
        if len(parts) > 0:
            new_path_info = f'{new_path_info}/{parts.pop(0)}'
        else:
            new_script_name = f'{new_script_name}/{parts.pop(0)}'
    return (new_script_name, new_path_info)