import os 
import typing

def peek_filelike_length(stream: typing.Any) -> typing.Optional[int]:
    try:
        fd = stream.fileno()
        length = os.fstat(fd).st_size
    except (AttributeError, OSError):
        try:
            offset = stream.tell()
            length = stream.seek(0, os.SEEK_END)
            stream.seek(offset)
        except (AttributeError, OSError):
            return None
    return length

