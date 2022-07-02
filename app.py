from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():  # put application's code here
    return '<h1>Welcome to Eric\'s Weather App!</h1>'


if __name__ == '__main__':
    app.run()
