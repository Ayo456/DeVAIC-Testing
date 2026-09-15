from typing import Any, Callable, List, Tuple


def parse_array(
    source: str,
    index: int,
    parse_value: Callable[[str, int], Tuple[int, Any]],
) -> Tuple[int, List[Any]]:
    n = len(source)

    if index >= n or source[index] != "[":
        raise SyntaxError(f"Expected '[' at position {index}")

    i = index + 1
    items: List[Any] = []

    def skip_whitespace_and_comments(pos: int) -> int:
        while pos < n:
            char = source[pos]
            if char in " \t\r\n":
                pos += 1
            elif char == "#":
                pos += 1
                while pos < n and source[pos] not in "\r\n":
                    pos += 1
            else:
                break
        return pos

    i = skip_whitespace_and_comments(i)
    if i < n and source[i] == "]":
        return i + 1, items

    expect_value = True

    while i < n:
        if expect_value:
            new_idx, val = parse_value(source, i)
            if new_idx == i:
                raise SyntaxError(f"Malformed value at position {i}")
            items.append(val)
            i = skip_whitespace_and_comments(new_idx)
            expect_value = False
        else:
            if i >= n:
                break
            char = source[i]
            if char == ",":
                i = skip_whitespace_and_comments(i + 1)
                expect_value = True
                if i < n and source[i] == "]":
                    return i + 1, items
            elif char == "]":
                return i + 1, items
            else:
                raise SyntaxError(
                    f"Expected ',' or ']' at position {i}, found {char!r}"
                )

    raise SyntaxError("Unclosed array: missing closing ']'")