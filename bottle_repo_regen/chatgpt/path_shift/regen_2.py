# regen 2
def path_shift(script_name: str, path_info: str, shift: int = 1) -> tuple[str, str]:
    script_parts = [part for part in script_name.split("/") if part]
    path_parts = [part for part in path_info.split("/") if part]

    if shift > 0:
        moved = path_parts[:shift]
        script_parts.extend(moved)
        path_parts = path_parts[shift:]

    elif shift < 0:
        amount = min(-shift, len(script_parts))
        moved = script_parts[-amount:] if amount else []
        script_parts = script_parts[:-amount] if amount else script_parts
        path_parts = moved + path_parts

    new_script_name = "/" + "/".join(script_parts) if script_parts else ""
    new_path_info = "/" + "/".join(path_parts) if path_parts else ""

    return new_script_name, new_path_info
