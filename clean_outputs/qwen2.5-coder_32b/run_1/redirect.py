from flask import Flask, redirect as flask_redirect, Response
app = Flask(__name__)

def redirect(url: str, code: int=None):
    if code is None:
        code = 303
    response = Response(status=code)
    response.headers['Location'] = url
    raise response

@app.route('/')
def index():
    try:
        redirect('https://www.example.com', 302)
    except Response as response:
        return response
if __name__ == '__main__':
    app.run(debug=True)

@app.route('/')
def index():
    return redirect('https://www.example.com', 302)