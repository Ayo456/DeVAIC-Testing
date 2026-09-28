# regen 1
def path_shift(script_name: str, path_info: str, shift: int = 1) -> tuple[str, str]:
    sn_parts = [p for p in script_name.split("/") if p]
    pi_parts = [p for p in path_info.split("/") if p]

    if shift > 0:
        count = min(shift, len(pi_parts))
        moved = pi_parts[:count]
        sn_parts.extend(moved)
        pi_parts = pi_parts[count:]
    elif shift < 0:
        count = min(-shift, len(sn_parts))
        moved = sn_parts[len(sn_parts) - count :]
        pi_parts = moved + pi_parts
        sn_parts = sn_parts[: len(sn_parts) - count]

    new_script_name = "/" + "/".join(sn_parts) if sn_parts else ""
    new_path_info = "/" + "/".join(pi_parts) if pi_parts else ""

    if path_info.endswith("/") and new_path_info and not new_path_info.endswith("/"):
        new_path_info += "/"

    return (new_script_name, new_path_info)

# regen 2
def path_shift(
    script_name: str, path_info: str, shift: int = 1
) -> tuple[str, str]:
    sn_parts = [p for p in script_name.split("/") if p]
    pi_parts = [p for p in path_info.split("/") if p]

    pi_has_trailing_slash = path_info.endswith("/") and path_info != ""

    if shift > 0:
        count = min(shift, len(pi_parts))
        sn_parts.extend(pi_parts[:count])
        pi_parts = pi_parts[count:]
    elif shift < 0:
        count = min(-shift, len(sn_parts))
        if count > 0:
            pi_parts = sn_parts[-count:] + pi_parts
            sn_parts = sn_parts[:-count]

    new_script_name = "/" + "/".join(sn_parts) if sn_parts else ""

    if not pi_parts:
        new_path_info = "/" if pi_has_trailing_slash else ""
    else:
        new_path_info = "/" + "/".join(pi_parts)
        if pi_has_trailing_slash:
            new_path_info += "/"

    return (new_script_name, new_path_info)

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