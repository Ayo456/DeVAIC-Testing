def path_shift(script_name: str, path_info: str, shift: int=1) -> tuple:
    parts_script = script_name.split('/')
    parts_path = path_info.split('/')
    if shift > 0:
        for _ in range(shift):
            if parts_path:
                parts_script.append(parts_path.pop(0))
    elif shift < 0:
        for _ in range(-shift):
            if parts_script:
                parts_path.insert(0, parts_script.pop())
    new_script_name = '/'.join(parts_script)
    new_path_info = '/'.join(parts_path)
    return (new_script_name, new_path_info)
script_name = '/users/'
path_info = 'profile/123'
new_script, new_path = path_shift(script_name, path_info, shift=2)
print(f'New script name: {new_script}')
print(f'New path info: {new_path}')
new_script, new_path = path_shift(script_name, path_info, shift=-1)
print(f'New script name: {new_script}')
print(f'New path info: {new_path}')