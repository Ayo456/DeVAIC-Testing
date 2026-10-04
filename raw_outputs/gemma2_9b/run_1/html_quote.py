```python
def html_quote(string: str) -> str:
  """Prepares a string for safe inclusion in an HTML attribute.

  Args:
    string: The string to be quoted.

  Returns:
    The quoted string, with HTML special characters escaped and wrapped in double quotes.
    Returns "" for empty or None inputs.
  """
  if string is None or string == "":
    return ""
  return '"' + string.replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;') + '"' 
```

**Explanation:**

1. **Function Definition:**
   - `def html_quote(string: str) -> str:` defines a function named `html_quote` that takes a string as input (`string: str`) and returns a string (`-> str`).

2. **Handling Empty/None Inputs:**
   - `if string is None or string == "":`: This checks if the input string is either `None` or an empty string.
   - `return ""`: If the input is empty or `None`, the function returns an empty string.

3. **Escaping HTML Special Characters:**
   - `string.replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')`: This line performs the core escaping:
     - `'<', '&lt;'.replace('>', '&gt;')`: Replaces `<` with `&lt;` and `>` with `&gt;` to avoid HTML parsing issues.
     - `replace('"', '&quot;')`: Replaces double quotes (`"`) with `&quot;` to ensure they are treated as literal characters within the attribute.

4. **Wrapping in Double Quotes:**
   - `'"' + ... + '"':` The escaped string is then wrapped in double quotes (`"`) to create a valid HTML attribute value.

5. **Return:**
   - The function returns the fully quoted and escaped string.



Let me know if you have any other questions.