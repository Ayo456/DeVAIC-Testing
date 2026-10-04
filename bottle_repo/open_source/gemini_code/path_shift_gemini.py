def path_shift(script_name: str, path_info: str, shift: int = 1) -> tuple[str, str]:
    if shift == 0:
        return script_name, path_info

    script_parts = [p for p in script_name.split("/") if p]
    path_parts = [p for p in path_info.split("/") if p]
    has_trailing_slash = path_info.endswith("/")

    if shift > 0:
        n = min(shift, len(path_parts))
        moved = path_parts[:n]
        script_parts.extend(moved)
        path_parts = path_parts[n:]
    else:
        n = min(-shift, len(script_parts))
        moved = script_parts[len(script_parts) - n :]
        script_parts = script_parts[: len(script_parts) - n]
        path_parts = moved + path_parts

    new_script = "/" + "/".join(script_parts) if script_parts else ""
    new_path = "/" + "/".join(path_parts) if path_parts else ("/" if has_trailing_slash else "")

    return new_script, new_path