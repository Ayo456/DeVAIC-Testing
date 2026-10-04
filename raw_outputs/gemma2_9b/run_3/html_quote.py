```python
def html_quote(string: str) -> str:
  """
  Prepares a string for safe inclusion in an HTML attribute.

  Args:
    string: The string to be quoted.

  Returns:
    The quoted string, with HTML special characters escaped and wrapped in double quotes.
    Returns "" for empty or None inputs.
  """
  if string is None or string == "":
    return ""
  return f'"{string.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")}"'

```

**Explanation:**

1. **Function Definition:**
   - `def html_quote(string: str) -> str:` defines a function named `html_quote` that takes a string argument (`string`) and is expected to return a string.
   - Type hints (`string: str` and `-> str`) are used for clarity and help with static analysis.

2. **Handling Empty or None Inputs:**
   - `if string is None or string == "":` checks if the input string is either `None` or an empty string.
   - If true, it immediately `return ""`, ensuring an empty quoted string is returned for these cases.

3. **Escaping HTML Special Characters:**
   - `string.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")` performs the core escaping logic:
     - `&` is replaced with `&amp;`
     - `<` is replaced with `&lt;`
     - `>` is replaced with `&gt;`
   - These replacements are necessary because these characters have special meanings in HTML and can cause unintended behavior if not escaped.

4. **Wrapping in Double Quotes:**
   - `f'"{escaped_string}"'` uses an f-string to create the final quoted string.
     - `"` encloses the escaped string in double quotes.

5. **Returning the Result:**
   - The function `return`s the fully quoted and escaped string.



Let me know if you have any more questions or want to explore other aspects of HTML sanitization!