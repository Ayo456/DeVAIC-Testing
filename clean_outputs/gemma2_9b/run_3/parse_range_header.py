def parse_range_header(header, maxlen=0):
    if not header or not header.startswith('bytes='):
        return
    for range_str in header.split('bytes=')[1].split(','):
        if '-' in range_str:
            parts = range_str.split('-')
            start = int(parts[0]) if parts[0] else maxlen
            end = int(parts[1]) if parts[1] else maxlen
            if start < 0:
                start = 0
            if end > maxlen:
                end = maxlen
            yield (start, end)