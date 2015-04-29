import os
import datetime
from flask import Flask, render_template
from models import db, Entry

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db.app = app
db.init_app(app)


@app.route('/')
def index():
    """Render the index page"""
    return flask.render_template('index.html')

@app.route('/all-entries-json')
def all_entries_json():
    """Return a JSON response containing all journal entries, for use
    with AJAX requests."""
    pass

if __name__ == "__main__":
    app.run()
