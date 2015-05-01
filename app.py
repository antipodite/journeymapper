import os
import datetime
from flask import Flask, render_template, jsonify
from models import db, Entry

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db.app = app
db.init_app(app)

@app.route('/')
def index():
    """Render the index page"""
    return render_template('index.html')

@app.route('/all-positions')
def all_entry_positions():
    """Return a JSON response containing all journal entry positions

    This is used to display all the positions where a journal entry
    was made on the Gmap when the index page is loaded. Position is
    given as a Gmaps coord literal"""
    rows = Entry.query.all()
    entries = {}
    for row in rows:
        entries[row.id] = {'lat': row.latitude, 'lng': row.longitude}
    return jsonify(entries)

@app.route('/entry-text/<eid>')
def text_for_entry(eid):
    """Return the text for specified entry primary key

    This is used in AJAX calls when the user clicks on a marker on
    the Gmap to load the text into the display box."""
    entry = Entry.query.get(eid).to_json()
    print type(entry)
    return jsonify(entry)

if __name__ == "__main__":
    app.run()
