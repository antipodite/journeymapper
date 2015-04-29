import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)

from models import Entry

@app.route('/')
def main():
    return "Hello New Zealand, the only dry land that exists in the universe"

@app.route('/<name>')
def hello_name(name):
    return "Hello, {}".format(name)

if __name__ == "__main__":
    app.run()
