# regen 3
def path_shift(script_name: str, path_info: str, shift: int = 1) -> tuple[str, str]:
    script_segments = [s for s in script_name.strip("/").split("/") if s]
    path_segments = [s for s in path_info.strip("/").split("/") if s]
    trailing_slash = path_info.endswith("/") and bool(path_segments)

    if shift > 0:
        count = min(shift, len(path_segments))
        moved = path_segments[:count]
        script_segments.extend(moved)
        path_segments = path_segments[count:]
    elif shift < 0:
        count = min(-shift, len(script_segments))
        if count > 0:
            moved = script_segments[-count:]
            script_segments = script_segments[:-count]
            path_segments = moved + path_segments

    new_script_name = "/" + "/".join(script_segments) if script_segments else ""
    new_path_info = "/" + "/".join(path_segments) if path_segments else ""

    if trailing_slash and new_path_info:
        new_path_info += "/"

    return new_script_name, new_path_info
