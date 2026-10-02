# regen 3
import html


def html_escape(string: str) -> str:
    """Escape HTML special characters (&, <, >, ", ') in the input.

    Converts non-string input to a string before escaping.
    """
    if not isinstance(string, str):
        string = str(string)

    return html.escape(string, quote=True)
