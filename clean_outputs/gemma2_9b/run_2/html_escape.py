def html_escape(string: str) -> str:
    if not isinstance(string, str):
        string = str(string)
    return string.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#039;')
text = 'This is some &lt;html&gt; with "quotes" and \'apostrophes!\''
escaped_text = html_escape(text)
print(escaped_text)