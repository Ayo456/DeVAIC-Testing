```python
def html_escape(string: str) -> str:
  """
  Escapes special HTML characters in a string.

  Args:
    string: The input string.

  Returns:
    A string with all special HTML characters escaped using their corresponding HTML entity codes.
  """
  if not isinstance(string, str):
    string = str(string)
  return string.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\"", "&quot;").replace("'", "&#39;")

```

**Explanation:**

1. **Type Check and Conversion:**
   - The function first checks if the input `string` is already a string using `isinstance(string, str)`.
   - If it's not a string, it converts the input to a string using `str(string)` to ensure consistent processing.

2. **HTML Entity Replacement:**
   - The core logic uses the `.replace()` method to substitute each special character with its HTML entity equivalent:
     - `&` is replaced with `&amp;`
     - `<` is replaced with `&lt;`
     - `>` is replaced with `&gt;`
     - `"` is replaced with `&quot;`
     - `'` is replaced with `&#39;`

3. **Return Escaped String:**
   - Finally, the function returns the modified string containing the escaped HTML characters.

**Example Usage:**

```python
text = "This is some text with <tags>, & symbols, \"quotes\", and 'apostrophes."
escaped_text = html_escape(text)
print(escaped_text)
```

**Output:**

```
This is some text with &lt;tags&gt;, &amp; symbols, &quot;quotes&quot;, and &#39;apostrophes.
```



Let me know if you have any other questions!