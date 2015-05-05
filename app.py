import os
from datetime import datetime
from flask import Flask, render_template, jsonify, request
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
    which have a valid latitude and longitude."""
    rows = Entry.query.filter(Entry.latitude != None, Entry.longitude != None)
    entries = {}
    for row in rows:
        entries[row.id] = row.to_latlng()
    return jsonify(entries)

@app.route('/entry-text/<eid>')
def text_for_entry(eid):
    """Return the text for specified entry primary key

    This is used in AJAX calls when the user clicks on a marker on
    the Gmap to load the text into the display box."""
    entry = Entry.query.get(eid).to_json()
    return jsonify(entry)

@app.route('/get-many-entries/<count>')
def get_many_entries(count):
    entries  = Entry.query.order_by(Entry.date.asc()).limit(count).all()
    return render_template('entry.html', entries=entries)

@app.route('/entries/')
def entries():
    start = datetime.strptime(request.args.get('start_date'), '%Y-%m-%d').date()
    count = request.args.get('count')
    entries = Entry.query.filter(Entry.date >= start).order_by(Entry.date.asc()).limit(count)
    return render_template('entry.html', entries=entries)

if __name__ == "__main__":
    app.run()
