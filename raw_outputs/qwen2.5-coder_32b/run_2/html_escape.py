Certainly! Below is the Python function `html_escape` that performs the required task. It ensures that the input is converted to a string if it's not already, and then it replaces special HTML characters with their corresponding HTML entity codes.

Here's the implementation:

```python
def html_escape(string: str) -> str:
    # Convert input to string if it's not already
    if not isinstance(string, str):
        string = str(string)
    
    # Define a mapping of special HTML characters to their entity codes
    html_entities = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#39;'
    }
    
    # Replace each special character with its corresponding entity code
    for char, entity in html_entities.items():
        string = string.replace(char, entity)
    
    return string

# Example usage:
print(html_escape("Hello & welcome to <Python>!"))  # Output: Hello &amp; welcome to &lt;Python&gt;!
print(html_escape(12345))  # Output: 12345
print(html_escape("It's a \"test\"."))  # Output: It&#39;s a &quot;test&quot;.
```

### Explanation:
1. **Input Conversion**: The function first checks if the input is a string. If not, it converts it to a string using `str(string)`.
2. **HTML Entities Mapping**: A dictionary `html_entities` is used to map special HTML characters to their corresponding HTML entity codes.
3. **Replacement**: The function iterates over the dictionary and replaces each occurrence of the special characters in the input string with their corresponding entity codes using the `replace` method.
4. **Return**: The function returns the modified string with all special HTML characters escaped.

This function should handle various types of inputs and correctly escape the specified HTML characters.