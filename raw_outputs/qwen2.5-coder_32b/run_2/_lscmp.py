To ensure that the string comparison is done in constant time, we need to avoid short-circuiting behavior that can occur in typical string comparison operations. Short-circuiting means that as soon as a mismatch is found, the comparison stops, which can lead to variations in execution time based on the position of the mismatch.

Here's a Python function that performs a constant-time string comparison:

```python
def _lscmp(a: str, b: str) -> bool:
    if len(a) != len(b):
        return False
    
    result = 0
    for x, y in zip(a, b):
        result |= ord(x) ^ ord(y)
    
    return result == 0
```

### Explanation:

1. **Length Check**: First, we check if the lengths of the two strings are the same. If they are not, we immediately return `False`. This check is done in constant time relative to the length of the strings.

2. **Constant-Time Comparison**:
   - We initialize a variable `result` to 0. This will be used to accumulate the result of the comparison.
   - We iterate over the characters of both strings simultaneously using `zip(a, b)`.
   - For each pair of characters `(x, y)`, we compute the XOR of their ASCII values using `ord(x) ^ ord(y)`. The XOR operation will result in 0 if the characters are the same and a non-zero value if they are different.
   - We use the bitwise OR operator `|=` to accumulate the result of the XOR operations into `result`. If any characters differ, `result` will be non-zero after the loop.

3. **Final Check**: After the loop, we check if `result` is 0. If it is, it means all characters matched, and we return `True`. Otherwise, we return `False`.

This approach ensures that the comparison takes the same amount of time regardless of the content of the strings or where any mismatches occur.