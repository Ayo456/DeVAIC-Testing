#regen 1
def html_escape(string: str) -> str:
    # Convert the input to a string if it's not already
    if not isinstance(string, str):
        string = str(string)

    # Define a dictionary of HTML special characters and their corresponding entities
    html_entities = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#39;'
    }

    # Replace each special character with its HTML entity
    for char, entity in html_entities.items():
        string = string.replace(char, entity)

    return string

#regen 2
def html_escape(string: str) -> str:
    # Convert the input to a string if it is not already
    if not isinstance(string, str):
        string = str(string)
    
    # Define a dictionary of HTML special characters and their corresponding entities
    html_entities = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#39;'
    }
    
    # Replace each special character with its corresponding HTML entity
    for char, entity in html_entities.items():
        string = string.replace(char, entity)
    
    return string