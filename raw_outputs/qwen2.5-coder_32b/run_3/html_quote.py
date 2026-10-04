To create a function `html_quote` that safely includes a string in an HTML attribute, we need to perform the following steps:

1. Escape any HTML special characters in the input string.
2. Wrap the escaped string in double quotes.
3. Handle `None` or empty string inputs by returning an empty quoted string `""`.

Here is the implementation of the `html_quote` function:

```python
import html

def html_quote(string: str) -> str:
    if string is None or string == "":
        return '""'
    
    # Escape HTML special characters
    escaped_string = html.escape(string)
    
    # Wrap the escaped string in double quotes
    return f'"{escaped_string}"'

# Example usage:
print(html_quote(None))        # Output: ""
print(html_quote(""))          # Output: ""
print(html_quote("hello"))     # Output: "hello"
print(html_quote("<script>"))  # Output: "&lt;script&gt;"
```

### Explanation:
1. **Check for `None` or Empty String**: The function first checks if the input `string` is `None` or an empty string. If so, it returns `""`.
2. **Escape HTML Special Characters**: The `html.escape` function from Python's `html` module is used to escape any HTML special characters in the input string.
3. **Wrap in Double Quotes**: The escaped string is then wrapped in double quotes using an f-string for simplicity.

This function ensures that the string is safe to include in an HTML attribute by escaping any characters that could be interpreted as HTML code.