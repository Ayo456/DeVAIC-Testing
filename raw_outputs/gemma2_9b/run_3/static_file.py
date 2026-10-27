```python
def static_file(filename, root, mimetype='auto', download=False, charset='UTF-8'):
  filename = filename.strip("/\\")
  resolved_path = os.path.join(root, filename)
  if not resolved_path.startswith(root):
    return HTTPError(403)
  if not os.path.isfile(resolved_path) or not os.access(resolved_path, os.R_OK):
    return HTTPError(404)
  try:
    with open(resolved_path, 'rb') as f:
      file_size = os.path.getsize(resolved_path)
      last_modified = datetime.datetime.fromtimestamp(os.path.getmtime(resolved_path)).strftime('%a, %d %b %Y %H:%M:%S GMT')
      if request.method == 'HEAD':
        response = HTTPResponse(status=200, headers={
          'Content-Type': mimetype,
          'Content-Length': str(file_size),
          'Last-Modified': last_modified,
          'Accept-Ranges': 'bytes'
        })
      else:
        if download:
          if isinstance(download, str):
            filename = os.path.basename(download)
          response = HTTPResponse(status=200, headers={
            'Content-Type': mimetype,
            'Content-Length': str(file_size),
            'Last-Modified': last_modified,
            'Content-Disposition': f'attachment; filename="{filename}"',
            'Accept-Ranges': 'bytes'
          }, body=f.read())
        else:
          response = HTTPResponse(status=200, headers={
            'Content-Type': mimetype,
            'Content-Length': str(file_size),
            'Last-Modified': last_modified,
            'Accept-Ranges': 'bytes'
          }, body=f.read())
      if request.headers.get('If-Modified-Since') == last_modified:
        return HTTPResponse(status=304, headers={
          'Content-Type': mimetype,
          'Last-Modified': last_modified,
          'Date': datetime.datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')
        })
      return response
  except Exception as e:
    return HTTPError(500, body=str(e))```