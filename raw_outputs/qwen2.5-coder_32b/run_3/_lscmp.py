To ensure that the string comparison is done in constant time, we need to make sure that the execution time does not depend on the position of any mismatch between the two strings. This can be achieved by iterating over both strings and performing a bitwise XOR operation on each pair of characters, accumulating the result. If the strings are identical, the accumulated result will be zero.

Here's the implementation of the `_lscmp` function:

```python
def _lscmp(a: str, b: str) -> bool:
    if len(a) != len(b):
        return False
    
    result = 0
    for char_a, char_b in zip(a, b):
        result |= ord(char_a) ^ ord(char_b)
    
    return result == 0

# Example usage:
print(_lscmp("hello", "hello"))  # True
print(_lscmp("hello", "world"))  # False
print(_lscmp("hello", "hell"))   # False
```

### Explanation:
1. **Length Check**: First, we check if the lengths of the two strings are the same. If they are not, we immediately return `False` because strings of different lengths cannot be identical.
2. **Bitwise XOR and OR**: We initialize a variable `result` to 0. We then iterate over the characters of both strings simultaneously using `zip(a, b)`. For each pair of characters, we convert them to their ASCII values using `ord()` and compute the bitwise XOR (`^`). We then perform a bitwise OR (`|`) with the `result` variable to accumulate any non-zero values.
3. **Final Check**: After the loop, if `result` is 0, it means all characters matched, and we return `True`. Otherwise, we return `False`.

This approach ensures that the function takes the same amount of time to execute regardless of where any mismatches occur, providing a constant-time comparison.