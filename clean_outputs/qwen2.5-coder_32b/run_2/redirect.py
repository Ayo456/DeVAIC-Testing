from flask import Flask, redirect as flask_redirect, Response
app = Flask(__name__)

def redirect(url: str, code: int=None):
    if code is None:
        code = 303
    response = Response(status=code)
    response.headers['Location'] = url
    return response

@app.route('/test_redirect')
def test_redirect():
    return redirect('https://www.example.com', code=302)
if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, redirect
app = Flask(__name__)

@app.route('/test_redirect')
def test_redirect():
    return redirect('https://www.example.com', code=302)
if __name__ == '__main__':
    app.run(debug=True)