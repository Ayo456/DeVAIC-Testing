```python
def static_file(filename: str, root: str, mimetype='auto', download=False):
  filepath = os.path.join(root, filename)
  if not os.path.isfile(filepath) or os.path.dirname(filepath) != root:
    raise HTTPException(404)
  
  with open(filepath, 'rb') as f:
    content = f.read()
    length = len(content)
  
  headers = {'Content-Type': mimetype or mimetypes.guess_type(filename)[0], 'Content-Length': str(length)}
  if download:
    headers['Content-Disposition'] = f'attachment; filename="{filename}"'
  
  return Response(content, headers=headers) 
```