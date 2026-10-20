def html_escape(string: str) -> str:
    if not isinstance(string, str):
        string = str(string)
    return string.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;')