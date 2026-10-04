```python
def html_quote(string: str) -> str:
  """Prepares a string for safe inclusion in an HTML attribute.

  Escapes HTML special characters and wraps the result in double quotes.
  Handles empty or None inputs by returning an empty quoted string "".

  Args:
    string: The string to be quoted.

  Returns:
    The quoted string, ready for use in an HTML attribute.
  """
  if string is None or string == "":
    return ""
  return '"' + string.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;') + '"'

```

**Explanation:**

1. **Function Definition:**
   - `def html_quote(string: str) -> str:` defines a function named `html_quote` that takes a string as input (`string: str`) and returns a string (`-> str`).

2. **Handling Empty or None Input:**
   - `if string is None or string == "":` checks if the input string is either `None` or an empty string.
   - `return ""` returns an empty string if the input is empty or `None`.

3. **Escaping HTML Characters:**
   - `string.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')` performs the core HTML escaping:
     - `&` is replaced with `&amp;`
     - `<` is replaced with `&lt;`
     - `>` is replaced with `&gt;`
     - `"` is replaced with `&quot;`

4. **Wrapping in Double Quotes:**
   - `'" + ... + "'"` adds double quotes around the escaped string.

5. **Return Statement:**
   - The function returns the fully quoted and escaped string.



Let me know if you have any other questions.