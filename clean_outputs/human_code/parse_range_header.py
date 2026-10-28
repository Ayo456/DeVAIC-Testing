def parse_range_header(header, maxlen=0):
    if not header or header[:6] != 'bytes=':
        return
    ranges = [r.split('-', 1) for r in header[6:].split(',') if '-' in r]
    for start, end in ranges:
        try:
            if not start:
                start, end = (max(0, maxlen - int(end)), maxlen)
            elif not end:
                start, end = (int(start), maxlen)
            else:
                start, end = (int(start), min(int(end) + 1, maxlen))
            if 0 <= start < end <= maxlen:
                yield (start, end)
        except ValueError:
            pass