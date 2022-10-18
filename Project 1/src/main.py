from flask import Flask, request
import requests
import psycopg2
# create the Flask app
app = Flask(__name__)



@app.route('/')
def index():
    return 'Index Page'


@app.route('/hello')
def hello():
    return 'Hello'


if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(debug=True, port=5000)