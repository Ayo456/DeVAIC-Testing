In this example:
- We import `Flask` and `redirect` from `flask`.
- We define a custom `redirect` function that constructs a `Response` object with the specified status code and `Location` header.
- We raise the `Response` object to trigger the redirection.
- In the `index` route, we demonstrate how to use the custom `redirect` function.

Note that raising a `Response` object to interrupt execution is a bit unconventional in Flask. Typically, you would just return the `Response` object, and Flask will handle the rest. However, since the task specifies raising an exception, this approach is used here.

If you want to stick to a more conventional approach in Flask, you can simply return the response object: