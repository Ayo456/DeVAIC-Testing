# regen 1
def path_shift(script_name: str, path_info: str, shift: int = 1) -> tuple[str, str]:
    if shift == 0:
        return script_name, path_info

    path_list = path_info.strip("/").split("/")
    script_list = script_name.strip("/").split("/")

    if path_list == [""]:
        path_list = []

    if script_list == [""]:
        script_list = []

    if shift > 0 and shift <= len(path_list):
        moved = path_list[:shift]
        script_list.extend(moved)
        path_list = path_list[shift:]

    elif shift < 0 and -shift <= len(script_list):
        moved = script_list[shift:]
        path_list = moved + path_list
        script_list = script_list[:shift]

    else:
        empty = "SCRIPT_NAME" if shift < 0 else "PATH_INFO"
        raise AssertionError(f"Cannot shift. Nothing left from {empty}")

    new_script_name = "/" + "/".join(script_list)
    new_path_info = "/" + "/".join(path_list)

    if path_info.endswith("/") and path_list:
        new_path_info += "/"

    return new_script_name, new_path_info

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

# regen 3
def path_shift(script_name: str, path_info: str, shift: int = 1) -> tuple[str, str]:
    if shift == 0:
        return script_name, path_info

    script_parts = [part for part in script_name.split("/") if part]
    path_parts = [part for part in path_info.split("/") if part]

    if shift > 0:
        if shift > len(path_parts):
            raise AssertionError("Cannot shift beyond PATH_INFO")

        script_parts.extend(path_parts[:shift])
        path_parts = path_parts[shift:]

    else:
        amount = -shift

        if amount > len(script_parts):
            raise AssertionError("Cannot shift beyond SCRIPT_NAME")

        path_parts = script_parts[-amount:] + path_parts
        script_parts = script_parts[:-amount]

    new_script_name = "/" + "/".join(script_parts) if script_parts else ""
    new_path_info = "/" + "/".join(path_parts) if path_parts else "/"

    return new_script_name, new_path_info