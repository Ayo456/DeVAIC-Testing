To create a function that safely includes a string in an HTML attribute, we need to escape any HTML special characters and then wrap the result in double quotes. HTML special characters that need to be escaped include `&`, `<`, `>`, `"`, and `'`. Python's `html` module provides a convenient function `html.escape()` that can handle most of these cases. However, since `html.escape()` does not escape double quotes by default, we will need to handle that separately.

Here's how you can implement the `html_quote` function:

```python
import html

def html_quote(string: str) -> str:
    if string is None or string == "":
        return '""'
    
    # Escape HTML special characters
    escaped_string = html.escape(string, quote=False)
    
    # Escape double quotes
    escaped_string = escaped_string.replace('"', '&quot;')
    
    # Wrap the result in double quotes
    return f'"{escaped_string}"'

# Example usage:
print(html_quote('Hello, "world"!'))  # Output: "Hello, &quot;world&quot;!"
print(html_quote('<div>Test</div>'))  # Output: "&lt;div&gt;Test&lt;/div&gt;"
print(html_quote(None))              # Output: ""
print(html_quote(''))                # Output: ""
```

### Explanation:
1. **Handling `None` and Empty Strings**: The function first checks if the input is `None` or an empty string. If so, it returns `""`.
2. **Escaping HTML Special Characters**: The `html.escape()` function is used to escape `&`, `<`, and `>`. The `quote=False` parameter ensures that single and double quotes are not escaped by `html.escape()`.
3. **Escaping Double Quotes**: After escaping other special characters, we manually replace any double quotes (`"`) with `&quot;`.
4. **Wrapping in Double Quotes**: Finally, the escaped string is wrapped in double quotes and returned.

This function ensures that the string is safe to include in an HTML attribute.