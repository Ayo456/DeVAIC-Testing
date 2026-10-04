To create a function that triggers an HTTP redirection in Python, you can use the `http.server` module for a simple HTTP server or a web framework like Flask for more complex applications. For this example, I'll use Flask, which is a popular web framework for Python.

First, you need to install Flask if you haven't already:

```sh
pip install Flask
```

Here's how you can implement the `redirect` function using Flask:

```python
from flask import Flask, redirect as flask_redirect, Response

app = Flask(__name__)

def redirect(url: str, code: int = None):
    if code is None:
        code = 303  # Default to 303 See Other

    # Create a response object with the desired status code
    response = Response(status=code)
    # Set the Location header
    response.headers['Location'] = url
    
    # Raise the response to trigger the redirection
    raise response

@app.route('/')
def index():
    try:
        redirect('https://www.example.com', 302)
    except Response as response:
        return response

if __name__ == '__main__':
    app.run(debug=True)
```

In this example:
- We import `Flask` and `redirect` from `flask`.
- We define a custom `redirect` function that constructs a `Response` object with the specified status code and `Location` header.
- We raise the `Response` object to trigger the redirection.
- In the `index` route, we demonstrate how to use the custom `redirect` function.

Note that raising a `Response` object to interrupt execution is a bit unconventional in Flask. Typically, you would just return the `Response` object, and Flask will handle the rest. However, since the task specifies raising an exception, this approach is used here.

If you want to stick to a more conventional approach in Flask, you can simply return the response object:

```python
@app.route('/')
def index():
    return redirect('https://www.example.com', 302)
```

This will achieve the same result without raising an exception.