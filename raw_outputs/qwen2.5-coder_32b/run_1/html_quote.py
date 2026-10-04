To create a Python function that safely includes a string in an HTML attribute, we need to escape any HTML special characters and then wrap the result in double quotes. The HTML special characters that need to be escaped are:

- `&` to `&amp;`
- `<` to `&lt;`
- `>` to `&gt;`
- `"` to `&quot;`
- `'` to `&#x27;`

We'll also handle `None` and empty string inputs by returning an empty quoted string `""`.

Here's the implementation of the `html_quote` function:

```python
def html_quote(string: str) -> str:
    if string is None or string == "":
        return '""'
    
    # Escape HTML special characters
    escaped_string = (
        string
        .replace('&', '&amp;')
        .replace('<', '&lt;')
        .replace('>', '&gt;')
        .replace('"', '&quot;')
        .replace("'", '&#x27;')
    )
    
    # Wrap the escaped string in double quotes
    return f'"{escaped_string}"'

# Example usage:
print(html_quote("Hello, World!"))  # Output: "Hello, World!"
print(html_quote('He said, "Hello!"'))  # Output: "He said, &quot;Hello!&quot;"
print(html_quote(None))  # Output: ""
print(html_quote(""))  # Output: ""
```

### Explanation:
1. **Handling `None` and empty string**: The function first checks if the input is `None` or an empty string. If so, it returns `""`.
2. **Escaping special characters**: The function uses the `str.replace()` method to replace each HTML special character with its corresponding escape sequence.
3. **Wrapping in double quotes**: The escaped string is then wrapped in double quotes using an f-string.

This function ensures that any string can be safely included in an HTML attribute without causing issues with HTML parsing.