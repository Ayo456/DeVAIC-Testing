def html_escape(string: str) -> str:
    s = str(string)
    table = {
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#x27;",
    }
    return "".join(table.get(char, char) for char in s)