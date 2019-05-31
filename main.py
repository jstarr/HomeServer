"""Starting point for our Flask Website"""

from flask import Flask

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return 'Hello World'

if __name__ == '__main__':
    print('-' * 25 + ' Starting... ' + '-' * 25)
    app.run(host="0.0.0.0", port=5000, debug=True)