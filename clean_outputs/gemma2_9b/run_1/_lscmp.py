def _lscmp(a, b):
    if len(a) != len(b):
        return False
    return all((c ^ d for c, d in zip(a, b)))