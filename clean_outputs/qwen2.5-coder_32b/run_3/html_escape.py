def html_escape(string: str) -> str:
    if not isinstance(string, str):
        string = str(string)
    html_entities = {'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'}
    for char, entity in html_entities.items():
        string = string.replace(char, entity)
    return string