```python
import functools
from flask import Flask, request, jsonify, make_response

def auth_basic(check_func):
  """
  Decorator for route handlers that implements HTTP Basic authentication.

  Args:
      check_func: A function that takes user and password arguments and returns True if authentication is successful, False otherwise.

  Returns:
      A wrapper function that handles authentication and calls the original route handler.
  """

  @functools.wraps(check_func)
  def wrapper(*args, **kwargs):
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
      return make_response(
          jsonify({'error': 'Authentication required'}), 401
      )
    
    if not check_func(auth.username, auth.password):
      return make_response(
          jsonify({'error': 'Invalid credentials'}), 401
      )

    return check_func(*args, **kwargs)  
  return wrapper

# Example usage:

app = Flask(__name__)

def check_credentials(username, password):
  """
  Example authentication function. Replace this with your actual logic.
  """
  return username == 'user' and password == 'password'

@app.route('/protected')
@auth_basic(check_credentials)
def protected_route():
  return jsonify({'message': 'Access granted!'})

if __name__ == '__main__':
  app.run(debug=True)
```

**Explanation:**

1. **`auth_basic` Decorator:**
   - Takes a `check_func` as an argument, which is the function responsible for authenticating users.
   - Uses `functools.wraps(check_func)` to preserve metadata of the original function.
   - Defines a `wrapper` function that handles authentication and calls the original function if successful.

2. **`wrapper` Function:**
   - Retrieves HTTP Basic authentication credentials from `request.authorization`.
   - Checks if credentials are present and valid. If not, returns a 401 Unauthorized response with an authentication challenge header:

     ```
     return make_response(
         jsonify({'error': 'Authentication required'}), 401
     )
     ```

   - Calls `check_func(auth.username, auth.password)` to perform the actual authentication check.
   - If authentication fails, returns a 401 Unauthorized response with an error message.

3. **`check_credentials` Function:**
   - This is a placeholder function that you need to replace with your own authentication logic. In the example, it simply checks if the username is "user" and the password is "password".

4. **Example Usage:**
   - The `@app.route('/protected')` and `@auth_basic(check_credentials)` lines demonstrate how to apply the decorator to a route handler.
   - The `protected_route` function is only accessible after successful authentication.

**Important Notes:**

- **Security:** This example uses simple in-memory authentication for demonstration purposes. In a real-world application, you should use a secure database or authentication system to store and verify user credentials.
- **Error Handling:** The code includes basic error handling for missing or invalid credentials. You should implement more robust error handling based on your application's requirements.



Let me know if you have any other questions or need further clarification!