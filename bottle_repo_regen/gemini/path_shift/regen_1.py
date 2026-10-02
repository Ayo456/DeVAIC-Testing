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
