def html_quote(string: str) -> str:
    if string is None or string == "":
        return '""'

    s = str(string)
    table = {
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#x27;",
    }
    escaped = "".join(table.get(char, char) for char in s)
    return f'"{escaped}"'