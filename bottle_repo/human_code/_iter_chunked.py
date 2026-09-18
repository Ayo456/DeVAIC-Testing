def _iter_chunked(self, read, bufsize):
    err = HTTPError(400, 'Error while parsing chunked transfer body.')
    rn, sem, bs = tob('\r\n'), tob(';'), tob('')
    while True:
        header = read(1)
        while header[-2:] != rn:
            c = read(1)
            header += c
            if not c: raise err
            if len(header) > bufsize: raise err
        size, _ = header.partition(sem)
        try:
            maxread = int(tonat(size.strip()), 16)
        except ValueError:
            raise err
        if maxread == 0: break
        buff = bs
        while maxread > 0:
            if not buff: buff = read(min(maxread, bufsize))
            part, buff = buff[:maxread], buff[maxread:]
            if not part: raise err
            yield part
            maxread -= len(part)
        if read(2) != rn: raise err
