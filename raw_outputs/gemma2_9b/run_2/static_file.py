```python
from http.server import HTTPServer, BaseHTTPRequestHandler
import os
from pathlib import Path

class StaticFileHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        filename = self.path[1:]  # Remove leading '/'

        # Construct the absolute path within the root directory
        root_path = Path(os.getcwd())
        requested_path = root_path / filename

        # Validate the path
        if not requested_path.exists() or not requested_path.is_file():
            self.send_error(404, "File not found")
            return

        # Prevent directory traversal
        if not requested_path.is_relative_to(root_path):
            self.send_error(403, "Forbidden")
            return

        # Set headers
        mimetype = self.get_content_type(filename)
        self.send_response(200)
        self.send_header("Content-type", mimetype)
        self.send_header("Content-length", str(os.path.getsize(str(requested_path))))
        self.end_headers()

        # Serve the file
        with open(str(requested_path), "rb") as f:
            self.wfile.write(f.read())

    def get_content_type(self, filename):
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

def run_static_server(root: str, port: int = 8000):
    """Run a simple static file server."""

    httpd = HTTPServer(("", port), StaticFileHandler)
    print(f"Serving static files at http://localhost:{port}/")
    httpd.serve_forever()

if __name__ == "__main__":
    root_dir = "/path/to/your/static/files"  # Replace with your actual root directory
    run_static_server(root_dir, 8000) 
```

**Explanation:**

1. **`StaticFileHandler` Class:**
   - Inherits from `BaseHTTPRequestHandler` to handle incoming HTTP requests.
   - **`do_GET()` Method:**
     - Extracts the requested filename from the request path (`self.path`).
     - Constructs the absolute path within the `root` directory using `Pathlib`.
     - **Validation:** Checks if the file exists and is within the `root` directory.
     - **Error Handling:** Returns a 404 error if the file is not found and a 403 error if it's outside the `root` directory.
     - **Headers:** Sets the `Content-type` header based on the file extension (using `get_content_type()`).
     - **Content Length:** Sets the `Content-length` header for efficient data transfer.
     - **File Serving:** Opens the file in binary read mode and writes its contents to the response stream (`self.wfile`).

2. **`get_content_type()` Method:**
   - A simple helper function to determine the appropriate `Content-type` based on the file extension.

3. **`run_static_server()` Function:**
   - Creates an `HTTPServer` instance, binding it to the specified port and using `StaticFileHandler` to handle requests.
   - Starts the server and prints a message to the console.

4. **`if __name__ == "__main__":` Block:**
   - When the script is executed directly, it sets the `root_dir` to your static files directory and calls `run_static_server()` to start the server.

**Remember:**

- Replace `/path/to/your/static/files` with the actual path to your static files directory.
- You can adjust the port number (default is 8000) as needed.



Let me know if you have any other questions or need further assistance!