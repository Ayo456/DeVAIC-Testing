import tomllib

def parse_array(src, pos, parse_float=float):
    if pos >= len(src) or src[pos] != "[":
        raise SyntaxError("Expected '[' at starting position")

    start = pos
    i = pos
    square_depth = 0
    curly_depth = 0

    quote = None
    multiline = False
    escaped = False
    in_comment = False

    while i < len(src):
        ch = src[i]

        if in_comment:
            if ch in "\r\n":
                in_comment = False
            i += 1
            continue

        if quote is not None:
            if multiline:
                if src.startswith(quote * 3, i):
                    i += 3
                    quote = None
                    multiline = False
                    escaped = False
                    continue

                if quote == '"' and ch == "\\":
                    i += 2
                    continue

                i += 1
                continue

            if quote == '"' and escaped:
                escaped = False
                i += 1
                continue

            if quote == '"' and ch == "\\":
                escaped = True
                i += 1
                continue

            if ch == quote:
                quote = None

            i += 1
            continue

        if ch == "#":
            in_comment = True
            i += 1
            continue

        if ch in ('"', "'"):
            if src.startswith(ch * 3, i):
                quote = ch
                multiline = True
                i += 3
            else:
                quote = ch
                multiline = False
                i += 1
            continue

        if ch == "[":
            square_depth += 1
            i += 1
            continue

        if ch == "]":
            square_depth -= 1

            if square_depth < 0:
                raise SyntaxError("Malformed array")

            if square_depth == 0 and curly_depth == 0:
                end = i + 1
                array_text = src[start:end]

                try:
                    result = tomllib.loads(
                        "value = " + array_text,
                        parse_float=parse_float
                    )["value"]
                except tomllib.TOMLDecodeError as exc:
                    raise SyntaxError(f"Malformed TOML array: {exc}") from exc

                return end, result

            i += 1
            continue

        if ch == "{":
            curly_depth += 1
        elif ch == "}":
            if curly_depth == 0:
                raise SyntaxError("Malformed array")
            curly_depth -= 1

        i += 1

    raise SyntaxError("Unclosed TOML array")