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
