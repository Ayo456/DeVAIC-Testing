To create a Python function that serves static files while ensuring security and proper HTTP headers, we can use the `os` and `mimetypes` modules to handle file paths and MIME types, and the `http.server` module to create a response object. However, since `http.server` is more suited for simple HTTP servers, we can use the `http` library to create a more robust solution, or use a web framework like Flask for simplicity.

Here, I'll demonstrate using Flask, a popular web framework, to create the `static_file` function. Flask provides a built-in way to serve static files, but we'll manually implement the logic to ensure we have full control over the response and security checks.

First, make sure you have Flask installed:
```sh
pip install Flask
```

Now, let's implement the `static_file` function:

```python
import os
import mimetypes
from werkzeug.exceptions import NotFound, Forbidden
from flask import Flask, Response, send_file

app = Flask(__name__)

def static_file(filename: str, root: str, mimetype='auto', download=False):
    # Resolve the full path to the file
    full_path = os.path.join(root, filename)
    
    # Normalize the path to prevent directory traversal attacks
    safe_path = os.path.abspath(full_path)
    
    # Ensure the resolved path is within the root directory
    if not safe_path.startswith(os.path.abspath(root) + os.sep):
        raise Forbidden("Access to the requested file is forbidden.")
    
    # Check if the file exists
    if not os.path.isfile(safe_path):
        raise NotFound("The requested file was not found.")
    
    # Determine the MIME type if auto
    if mimetype == 'auto':
        mimetype, _ = mimetypes.guess_type(safe_path)
        if mimetype is None:
            mimetype = 'application/octet-stream'
    
    # Create a response object
    response = send_file(
        safe_path,
        mimetype=mimetype,
        as_attachment=download,
        download_name=os.path.basename(safe_path) if download else None
    )
    
    return response

# Example usage within a Flask route
@app.route('/static/<path:filename>')
def serve_static(filename):
    try:
        return static_file(filename, root='/path/to/static/files', mimetype='auto', download=False)
    except (NotFound, Forbidden) as e:
        return str(e), 404 if isinstance(e, NotFound) else 403

if __name__ == '__main__':
    app.run(debug=True)
```

### Explanation:

1. **Path Resolution and Normalization**:
   - We use `os.path.join` to construct the full path to the requested file.
   - We then normalize this path using `os.path.abspath` to resolve any relative path components.
   - We check if the normalized path starts with the absolute path of the root directory to prevent directory traversal attacks.

2. **File Existence Check**:
   - We use `os.path.isfile` to check if the file exists at the resolved path.

3. **MIME Type Determination**:
   - We use `mimetypes.guess_type` to determine the MIME type of the file. If it can't determine the type, we default to `application/octet-stream`.

4. **Response Creation**:
   - We use Flask's `send_file` to create a response object. This function handles setting the appropriate headers and streaming the file content.
   - The `as_attachment` parameter is set based on the `download` flag to determine if the file should be served as a download or inline.

5. **Error Handling**:
   - We raise `NotFound` if the file does not exist and `Forbidden` if the path is outside the root directory.
   - In the Flask route, we handle these exceptions and return the appropriate HTTP status codes.

This function provides a secure way to serve static files while ensuring that the resolved path remains within the specified root directory.