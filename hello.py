from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return '<p>Hello World</p>'

@app.route('/user/<name>')
def user(name):
    return '<p>the user is %s</p>' % name

if __name__ == '__main__':
    app.run(debug=True)

