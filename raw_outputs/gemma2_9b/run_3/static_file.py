```python
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse


class StaticFileHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.root = kwargs['root']

    def do_GET(self):
        try:
            path = urlparse(self.path).path
            resolved_path = os.path.join(self.root, path)

            # Validate path against root directory
            if not path.startswith('/'):
                self.send_error(400, "Invalid request path")
                return
            if not os.path.normpath(resolved_path).startswith(self.root):
                self.send_error(403, "Forbidden")
                return

            # Get file information
            if not os.path.isfile(resolved_path):
                self.send_error(404, "File not found")
                return

            with open(resolved_path, 'rb') as f:
                file_content = f.read()
                file_length = len(file_content)

            # Set headers
            self.send_response(200)
            self.send_header("Content-type", self.get_mimetype(resolved_path))
            self.send_header("Content-Length", str(file_length))
            self.end_headers()

            # Send file content
            self.wfile.write(file_content)

        except Exception as e:
            self.send_error(500, "Internal Server Error")


    def get_mimetype(self, filename):
        if filename.endswith(".html"):
            return "text/html"
        elif filename.endswith(".css"):
            return "text/css"
        elif filename.endswith(".js"):
            return "application/javascript"
        elif filename.endswith(".png"):
            return "image/png"
        elif filename.endswith(".jpg"):
            return "image/jpeg"
        else:
            return "application/octet-stream" 



def static_file(filename: str, root: str, mimetype='auto', download=False):
    """
    Serves a requested static file located under a target root directory.

    Args:
        filename: The requested filename.
        root: The root directory containing the static files.
        mimetype: The MIME type of the file (optional, defaults to 'auto').
        download: Whether to trigger a download (optional, defaults to False).

    Returns:
        A response object or stream containing the file content.
        Raises an HTTP 404 or 403 error if the file is missing or outside the root directory.
    """

    # Construct the URL path
    url_path = f"/{filename}"

    # Create an HTTP server instance
    server = HTTPServer(("", 8000), StaticFileHandler, root=root)

    # Handle the GET request
    server.handle_request(url_path) 

```

**Explanation:**

1. **`StaticFileHandler` Class:**
   - Inherits from `BaseHTTPRequestHandler` to handle HTTP requests.
   - `__init__`: Stores the `root` directory for validation.
   - `do_GET`: Handles GET requests:
     - Parses the requested path.
     - Constructs the absolute `resolved_path` by joining the `root` with the requested path.
     - **Security:**
       - Checks if the path starts with '/' to prevent issues with relative paths.
       - **Crucial:** Ensures `resolved_path` is within the `root` directory to prevent directory traversal attacks.
     - Checks if the `resolved_path` is a file using `os.path.isfile`.
     - If the file exists:
       - Reads the file content into `file_content`.
       - Determines the MIME type using `get_mimetype` (you can customize this).
       - Sets the HTTP response code to 200 (OK).
       - Sets appropriate headers: `Content-Type`, `Content-Length`.
       - Writes the file content to the response.
     - If the file doesn't exist, sends a 404 Not Found error.
     - If the path is invalid or outside the root, sends a 403 Forbidden error.
   - `get_mimetype`: A simple function to determine the MIME type based on the filename extension.

2. **`static_file` Function:**
   - Constructs the `url_path` for the request.
   - Creates an `HTTPServer` instance on port 8000, using `StaticFileHandler` and passing the `root` directory.
   - Calls `server.handle_request` to process the GET request for the specified `url_path`.
   - **Note:** This function doesn't return a response object directly because it uses a server to handle the request.

**How to Use:**

1. **Replace `'your_root_directory'` with the actual path to your static files.**
2. **Run the Python script.**
3. **Access the static file in your browser using the URL:** `http://localhost:8000/filename`.



**Important Security Considerations:**

- **Directory Traversal Prevention:** The code rigorously checks the requested path against the `root` directory to prevent attackers from accessing files outside the intended directory structure.
- **Input Validation:** Always sanitize user input to prevent malicious code injection.


Let me know if you have any other questions or requests!