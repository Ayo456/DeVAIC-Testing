```python
def static_file(filename: str, root: str, mimetype='auto', download=False):
  filepath = os.path.join(root, filename)
  if not os.path.exists(filepath) or os.path.normpath(filepath).startswith(os.path.normpath(root) + os.path.sep):
    raise HTTPException(404)
  headers = {'Content-Type': mimetype if mimetype != 'auto' else mimetypes.guess_type(filename)[0]}
  if download:
    headers['Content-Disposition'] = 'attachment; filename=' + filename
  return FileResponse(filepath, headers=headers)
```