import functools
from flask import Flask, request, jsonify, make_response

def auth_basic(check_func):

    @functools.wraps(check_func)
    def wrapper(*args, **kwargs):
        auth = request.authorization
        if not auth or not auth.username or (not auth.password):
            return make_response(jsonify({'error': 'Authentication required'}), 401)
        if not check_func(auth.username, auth.password):
            return make_response(jsonify({'error': 'Invalid credentials'}), 401)
        return check_func(*args, **kwargs)
    return wrapper
app = Flask(__name__)

def check_credentials(username, password):
    return username == 'user' and password == 'password'

@app.route('/protected')
@auth_basic(check_credentials)
def protected_route():
    return jsonify({'message': 'Access granted!'})
if __name__ == '__main__':
    app.run(debug=True)