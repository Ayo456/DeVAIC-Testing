Certainly! Below is a Python function named `html_escape` that takes a string as input and returns a new string with all special HTML characters replaced by their corresponding HTML entity codes. If the input is not a string, it converts the input to its string representation first.

Here's the implementation:

```python
def html_escape(string: str) -> str:
    # Convert input to string if it's not already a string
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

# Example usage:
if __name__ == "__main__":
    test_string = "Hello & welcome to <example> world! 'It's a test.'"
    print(html_escape(test_string))  # Output: Hello &amp; welcome to &lt;example&gt; world! &apos;It&apos;s a test.&apos;
    
    non_string_input = 12345
    print(html_escape(non_string_input))  # Output: 12345
```

### Explanation:
1. **Type Checking and Conversion**: The function first checks if the input is a string. If not, it converts the input to a string using `str(string)`.
2. **HTML Entities Dictionary**: A dictionary `html_entities` is defined to map special HTML characters to their corresponding HTML entity codes.
3. **Replacement Loop**: The function iterates over the dictionary and replaces each occurrence of the special character in the input string with its corresponding HTML entity.
4. **Return the Result**: Finally, the function returns the modified string.

This function ensures that any special HTML characters in the input are properly escaped, and it handles non-string inputs gracefully by converting them to strings first.