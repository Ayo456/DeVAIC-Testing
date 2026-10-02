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
