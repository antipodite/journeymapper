import os
import datetime
from flask import Flask
from models import db, Entry

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db.init_app(app)


@app.route('/')
def main():
    return "Hello New Zealand, the only dry land that exists in the universe"

if __name__ == "__main__":
    app.run()
