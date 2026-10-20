from pathlib import Path

def static_file(filename: str, root: str, mimetype='auto', download=False):
    filepath = Path(root, filename)
    if filepath.exists() and filepath.is_file() and (filepath.resolve().parents[0] == Path(root)):
        if mimetype == 'auto':
            mimetype = filepath.suffix[1:].lower()
        headers = {'Content-Type': f'{mimetype}', 'Content-Length': str(filepath.stat().st_size)}
        if download:
            headers['Content-Disposition'] = f'attachment; filename="{filename}"'
        return (filepath.open('rb'), headers)
    else:
        raise HTTPException(404)