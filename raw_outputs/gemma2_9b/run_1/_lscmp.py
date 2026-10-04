```python
def _lscmp(a: str, b: str) -> bool:
    """
    Compares two strings for equality in constant time.

    Args:
      a: The first string.
      b: The second string.

    Returns:
      True if the strings are identical, otherwise False.
    """
    result = 0
    for i in range(min(len(a), len(b))):
        result |= ord(a[i]) ^ ord(b[i])
    return result == 0 and len(a) == len(b) 
```

**Explanation:**

1. **Initialization:**
   - `result = 0`: We start with a variable `result` initialized to 0. This variable will accumulate the bitwise XOR results of comparing characters.

2. **Iterating through Characters:**
   - `for i in range(min(len(a), len(b))):`:  The loop iterates through the characters of both strings, considering only the length of the shorter string to avoid index errors.

3. **Bitwise XOR Comparison:**
   - `result |= ord(a[i]) ^ ord(b[i])`: 
     - `ord(a[i])` and `ord(b[i])` convert the characters at position `i` in strings `a` and `b` to their ASCII (numerical) representations.
     - `^` performs a bitwise XOR operation on the ASCII values. If the characters are the same, the XOR result is 0; otherwise, it's non-zero.
     - `|=` performs a bitwise OR assignment, effectively setting a bit in `result` if any character comparison yields a non-zero XOR result.

4. **Final Check and Return:**
   - `return result == 0 and len(a) == len(b)`: 
     - `result == 0`:  If `result` remains 0 after comparing all characters, it means all characters were identical.
     - `len(a) == len(b)`: We also check if the lengths of the strings are equal, as a different length implies inequality even if characters match up to the shorter length.

**Constant Time:**

The key to constant time complexity is that the number of operations (bitwise XORs and assignments) is fixed, regardless of where mismatches occur in the strings. 

Let me know if you have any more questions!