Certainly! Below is a Python function named `html_escape` that takes a string as input and returns a new string with all special HTML characters replaced by their corresponding HTML entity codes. If the input is not a string, it first converts it to a string representation.

```python
def html_escape(string: str) -> str:
    # Ensure the input is a string
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

# Example usage:
# print(html_escape("<div class='example'>Hello & welcome!</div>"))
# Output: &lt;div class=&#39;example&#39;&gt;Hello &amp; welcome!&lt;/div&gt;
```

This function works by first checking if the input is a string. If not, it converts it to a string using `str()`. It then iterates over a dictionary of HTML special characters and their corresponding entities, replacing each occurrence of the special character in the input string with its entity. Finally, it returns the escaped string.