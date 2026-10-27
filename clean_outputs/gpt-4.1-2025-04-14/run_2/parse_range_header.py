def parse_range_header(header, maxlen=0):
    if not header or not header.startswith('bytes=') or maxlen <= 0:
        return
    ranges = header[6:].split(',')
    for r in ranges:
        r = r.strip()
        if '-' not in r:
            continue
        if r.startswith('-'):
            try:
                n = int(r[1:])
            except ValueError:
                continue
            if n <= 0:
                continue
            start = max(0, maxlen - n)
            end = maxlen
        else:
            parts = r.split('-', 1)
            try:
                start = int(parts[0])
            except ValueError:
                continue
            if parts[1] == '':
                end = maxlen
            else:
                try:
                    end = int(parts[1]) + 1
                except ValueError:
                    continue
            if start >= maxlen or start < 0:
                continue
            if end > maxlen:
                end = maxlen
            if end <= start:
                continue
        if 0 <= start < end <= maxlen:
            yield (start, end)