To create a function that compares two strings for equality in constant time, we need to ensure that the comparison does not depend on the position of the first mismatch. This can be achieved by iterating over the strings and using a constant-time comparison technique. One common approach is to use a bitwise XOR operation and accumulate the results. If the strings are identical, the accumulated result will be zero.

Here's how you can implement this in Python:

```python
def _lscmp(a: str, b: str) -> bool:
    # If the lengths of the strings are not the same, they cannot be equal
    if len(a) != len(b):
        return False
    
    # Initialize a variable to accumulate the result of XOR operations
    result = 0
    
    # Iterate over the characters of the strings
    for char_a, char_b in zip(a, b):
        # Perform XOR operation between the ASCII values of the characters
        result |= ord(char_a) ^ ord(char_b)
    
    # If result is 0, the strings are identical
    return result == 0

# Example usage:
print(_lscmp("hello", "hello"))  # Output: True
print(_lscmp("hello", "world"))  # Output: False
print(_lscmp("hello", "hell"))   # Output: False
```

### Explanation:
1. **Length Check**: First, we check if the lengths of the two strings are the same. If they are not, we immediately return `False` because strings of different lengths cannot be identical.
2. **XOR Accumulation**: We initialize a variable `result` to 0. We then iterate over the characters of both strings simultaneously using `zip`. For each pair of characters, we compute the XOR of their ASCII values and use the bitwise OR (`|=`) to accumulate the result.
3. **Result Check**: After the loop, if `result` is 0, it means all corresponding characters in the two strings were identical, so we return `True`. Otherwise, we return `False`.

This approach ensures that the time taken to compare the strings does not depend on the position of any mismatch, thus providing constant time complexity for the comparison.