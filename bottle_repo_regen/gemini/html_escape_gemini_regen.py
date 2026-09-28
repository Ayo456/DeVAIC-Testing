# regen 1
import html


def html_escape(string: str) -> str:
    return html.escape(str(string), quote=True)

# regen 2
import html


def html_escape(string: str) -> str:
    """Escape special HTML characters (&, <, >, ", ') into their corresponding entity codes."""
    if not isinstance(string, str):
        string = str(string)

    return html.escape(string, quote=True)

# regen 3
import html


def html_escape(string: str) -> str:
    """Escape HTML special characters (&, <, >, ", ') in the input.

    Converts non-string input to a string before escaping.
    """
    if not isinstance(string, str):
        string = str(string)

    return html.escape(string, quote=True)