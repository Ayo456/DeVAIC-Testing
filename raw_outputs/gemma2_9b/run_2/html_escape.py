```python
def html_escape(string: str) -> str:
  """
  Escapes special HTML characters in a string.

  Args:
    string: The input string to escape.

  Returns:
    A new string with HTML entities replacing special characters.
  """
  if not isinstance(string, str):
    string = str(string)
  return string.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\"", "&quot;").replace("'", "&#039;") 

# Example usage
text = "This is some &lt;html&gt; with \"quotes\" and 'apostrophes!'"
escaped_text = html_escape(text)
print(escaped_text)
```

**Explanation:**

1. **Function Definition:**
   - `def html_escape(string: str) -> str:` defines a function named `html_escape` that takes a single argument `string` of type `str` and returns a string (`-> str`).

2. **Type Check and Conversion:**
   - `if not isinstance(string, str):`: Checks if the input `string` is actually a string.
   - `string = str(string)`: If it's not a string, it converts the input to a string using `str(string)`.

3. **HTML Entity Replacement:**
   - `string.replace("&", "&amp;")`: Replaces all ampersands (`&`) with `&amp;`.
   - `string.replace("<", "&lt;")`: Replaces all less than signs (`<`) with `&lt;`.
   - `string.replace(">", "&gt;")`: Replaces all greater than signs (>) with `&gt;`.
   - `string.replace("\"", "&quot;")`: Replaces all double quotes (`"`) with `&quot;`.
   - `string.replace("'", "&#039;")`: Replaces all single quotes (') with `&#039;`.

4. **Return Escaped String:**
   - The function returns the modified string with the HTML entities replaced.

**Example Usage:**

- The provided example demonstrates how to use the function:
   - It creates a string with HTML characters.
   - It calls `html_escape()` to escape the string.
   - It prints the escaped string, which will now be safe to use in HTML without causing rendering issues.



Let me know if you have any other questions.