To achieve HTTP redirection in a Python web application, you typically use a web framework like Flask or Django. However, since the task is to write a generic function that constructs an HTTP response and raises an exception to interrupt execution, I'll create a function that mimics this behavior using the `http.client` module for constructing the response and raising a custom exception.

Here's how you can implement this:

1. Define a custom exception for HTTP responses.
2. Create the `redirect` function that constructs the HTTP response and raises the custom exception.

First, let's define a custom exception:

```python
class HTTPResponseException(Exception):
    def __init__(self, status_code: int, headers: dict, body: str = ''):
        self.status_code = status_code
        self.headers = headers
        self.body = body
        super().__init__(f"HTTP Response: {status_code}")

    def __str__(self):
        header_str = '\n'.join(f"{k}: {v}" for k, v in self.headers.items())
        return f"{self.status_code} HTTP Response\nHeaders:\n{header_str}\n\nBody:\n{self.body}"
```

Next, let's implement the `redirect` function:

```python
def redirect(url: str, code: int = None):
    # Default to 303 for HTTP/1.1 and above, 302 for HTTP/1.0
    if code is None:
        code = 303  # Assuming HTTP/1.1 or above

    headers = {
        'Location': url
    }

    # Construct the response body (optional)
    body = f"Redirecting to {url}"

    # Raise the HTTPResponseException with the constructed response
    raise HTTPResponseException(code, headers, body)
```

Here's how you can use the `redirect` function:

```python
try:
    redirect("https://example.com", 302)
except HTTPResponseException as e:
    print(e)
```

This will output:
```
302 HTTP Response
Headers:
Location: https://example.com

Body:
Redirecting to https://example.com
```

This function constructs an HTTP response with a `Location` header and raises an `HTTPResponseException` to interrupt execution. The `HTTPResponseException` class is designed to hold the status code, headers, and body of the HTTP response, and it can be used to simulate the behavior of an HTTP redirection in a web application.