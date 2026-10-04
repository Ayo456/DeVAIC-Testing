def html_escape(string: str) -> str:
    if not isinstance(string, str):
        string = str(string)
    html_entities = {'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'}
    for char, entity in html_entities.items():
        string = string.replace(char, entity)
    return string
if __name__ == '__main__':
    test_string = "Hello & welcome to <example> world! 'It's a test.'"
    print(html_escape(test_string))
    non_string_input = 12345
    print(html_escape(non_string_input))