import os


def peek_filelike_length(stream):
        try:
        fileno = stream.fileno()
        return os.fstat(fileno).st_size
    except (AttributeError, OSError, TypeError, ValueError):
        pass

    try:
        original_position = stream.tell()

        stream.seek(0, os.SEEK_END)
        length = stream.tell()

        stream.seek(original_position)
        return length

    except (AttributeError, OSError, TypeError, ValueError):
        try:
            stream.seek(original_position)
        except (AttributeError, OSError, TypeError, ValueError, UnboundLocalError):
            pass

        return None