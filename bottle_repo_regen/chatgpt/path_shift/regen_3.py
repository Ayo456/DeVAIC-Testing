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
