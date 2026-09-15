import io
import os
from typing import Any, Optional

def peek_filelike_length(stream: Any) -> Optional[int]:
    try:
        fd = stream.fileno()
        return os.fstat(fd).st_size
    except (AttributeError, OSError, io.UnsupportedOperation):
        pass

    try:
        cur_pos = stream.tell()
        stream.seek(0, io.SEEK_END)
        size = stream.tell()
        stream.seek(cur_pos, io.SEEK_SET)
        return size
    except (AttributeError, OSError, io.UnsupportedOperation):
        pass

    return None