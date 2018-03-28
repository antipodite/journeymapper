import os
from datetime import datetime
from flask import Flask, render_template, jsonify, request
from models import db, Entry

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db.app = app
db.init_app(app)

def make_linestring_from_latlngs(latlngs):
    """Construct a GeoJSON linestring from a list of coordinates"""
    ls = {'type': 'LineString'}
    ls['coordinates'] = [[l['lng'], l['lat']] for l in latlngs]
    return ls

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

@app.route('/journals/<jid>')
def get_route_for_journal(jid):
    """Return a GeoJSON Linestring representing the route taken in
    this journal.
    """
    query = Entry.query.filter(Entry.latitude != None,
                               Entry.longitude != None,
                               Entry.journal_id == jid)
    entries = query.all()
    coords = [entry.to_latlng() for entry in entries]
    linestring = make_linestring_from_latlngs(coords)
    return jsonify(linestring)

@app.route('/entries/query/')
def query_entries():
    """Allow the browser to query the entry table - accepts optional
    arguments, constructs SQLAlchemy query, then returns rendered entries
    """
    # There are some parameters
    if request.args:
        query = db.session.query(Entry).order_by(Entry.date.asc())

        start_date = request.args.get('start_date')
        if start_date:
            start = datetime.strptime(start_date, '%Y-%m-%d').date()
            query = query.filter(Entry.date > start)

        end_date = request.args.get('end_date')
        if end_date:
            end = datetime.strptime(end_date, '%Y-%m-%d)').date()
            query = query.filter(Entry.date < end)

        eid = request.args.get('eid')
        if eid:
            query = query.filter(Entry.id >= eid)

        # This has to come after any .filter calls or SQLAlchemy complains
        count = request.args.get('count')
        if count:
            query = query.limit(count)

        entries = query.all()

    # There are no parameters
    else:
        entries = []

    return render_template('entry.html', entries=entries)

if __name__ == "__main__":
    app.run()
