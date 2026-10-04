```python
def html_escape(string: str) -> str:
  """
  Escapes special HTML characters in a string.

  Args:
    string: The input string to escape.

  Returns:
    A string with special HTML characters replaced by their entity codes.
  """
  if not isinstance(string, str):
    string = str(string)
  return string.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#039;') 
```

**Explanation:**

1. **Function Definition:**
   - `def html_escape(string: str) -> str:`: Defines a function named `html_escape` that takes a string (`string`) as input and returns a string.

2. **Type Hinting:**
   - `string: str`: Specifies that the input `string` should be a string.
   - `-> str`: Indicates that the function returns a string.

3. **Input Type Check:**
   - `if not isinstance(string, str):`: Checks if the input is not already a string.
   - `string = str(string)`: If it's not a string, convert it to a string using `str(string)`.

4. **HTML Escaping:**
   - `string.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#039;')`: This line performs the core escaping operation. It uses the `replace()` method to substitute each special character with its corresponding HTML entity code:
     - `&` becomes `&amp;`
     - `<` becomes `&lt;`
     - `>` becomes `&gt;`
     - `"` becomes `&quot;`
     - `'` becomes `&#039;`

5. **Return Value:**
   - The function returns the modified string with escaped characters.



**Example Usage:**

```python
text = "I have some <script> code and &quot;quotes&quot;."
escaped_text = html_escape(text)
print(escaped_text) 
```

**Output:**

```
I have some &lt;script&gt; code and &amp;quot;quotes&amp;quot;.
```