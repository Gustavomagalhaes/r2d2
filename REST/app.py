#!flask/bin/python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World! R2D2 here!"

if __name__ == '__main__':
    app.run(debug=False)
    # app.run(host='http://172.17.25.80', port=500)