def path_shift(script_name: str, path_info: str, shift: int = 1):
    script_parts = [p for p in script_name.split("/") if p]
    path_parts = [p for p in path_info.split("/") if p]

    if shift > 0:
        if shift > len(path_parts):
            raise ValueError("Not enough path segments to shift")
        script_parts.extend(path_parts[:shift])
        path_parts = path_parts[shift:]

    elif shift < 0:
        count = -shift
        if count > len(script_parts):
            raise ValueError("Not enough script segments to shift")
        path_parts = script_parts[-count:] + path_parts
        script_parts = script_parts[:-count]

    new_script_name = "/" + "/".join(script_parts) if script_parts else ""
    new_path_info = "/" + "/".join(path_parts) if path_parts else "/"

    return new_script_name, new_path_info