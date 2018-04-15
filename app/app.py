import os
import sys

from datetime import datetime
from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from app.config import DevConfig, LiveConfig
from database.models import Journal, Entry, Metadata
from app.models import User

## Configure app

app = Flask(__name__)

if os.environ['APP_ENV'] == 'live':
    settings = LiveConfig
else:
    settings = DevConfig
app.config.from_object(settings)

## DB configuration

db = SQLAlchemy(app, metadata=Metadata)
db.create_all()
session = db.session

## User login support

login_manager = LoginManager()
login_manager.init_app(app)

## Views

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/journal/<jid>/render')
def render_journal_data(jid):
    '''
    Retrieve journal and all associated entries by ID from database,
    construct a GeoJSON object from them, and return it to client.
    '''
    geojson = session.query(Journal).get(jid).to_geojson()
    
    return jsonify(geojson)

@app.route('/entry-text/<eid>')
def text_for_entry(eid):
    '''
    Return the text for specified entry primary key
    '''
    entry = session.query(Entry).get(eid)
    print(entry)
    return jsonify(entry)

if __name__ == "__main__":
    app.run(use_reloader=False)
