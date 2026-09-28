# regen 1
def html_escape(string: str) -> str:
    string = str(string)

    return (
        string.replace("&", "&amp;")
              .replace("<", "&lt;")
              .replace(">", "&gt;")
              .replace('"', "&quot;")
              .replace("'", "&#x27;")
    )

# regen 2
def html_escape(string: str) -> str:
    string = str(string)
    return (
        string.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#39;")
    )

# regen 3
import html

def html_escape(string: str) -> str:
    return html.escape(str(string), quote=True)