import os
import sys
import json
from json import JSONDecodeError

from datetime import datetime
from flask import Flask, render_template, jsonify, request, flash, abort, redirect, url_for

from flask_sqlalchemy import SQLAlchemy

from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

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

# Create admin user if it doesn't exist. TODO: Find better way of doing this 
# that doesn't need password in source code
if not db.session.query(User).filter_by(name='admin').first():
    admin_user = User(name='admin', email='admin@navigato.rs')
    adminpw = os.environ['ADMIN_PASSWORD']
    admin_user.set_password(adminpw)
    db.session.add(admin_user)
    db.session.commit()

## User login support

login_manager = LoginManager()
login_manager.init_app(app)

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Sign in')

@login_manager.user_loader
def load_user(userid):
    return session.query(User).get(userid)

## File upload support

class UploadForm(FlaskForm):
    journal_file = FileField(validators=[
        FileRequired(),
        FileAllowed(['json'], 'json only')
    ])
    submit = SubmitField('Upload')

## Views

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        # TODO flashing messages requires support in template
        try:
            user = session.query(User).filter_by(name=username).first()
            login_user(user)
            flash('Logged in successfully.')
            next = request.args.get('next')
            #if not is_safe_url(next):
            #    return abort(400)
            return redirect(next or url_for('index'))
        except AttributeError:
            form.errors['user_missing'] = 'No user named ' + username

    return render_template('login.html', title='Log in', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = UploadForm()
    if form.validate_on_submit() and current_user.name == 'admin':
        f = form.journal_file.data
        try:
            data = f.read().decode('utf-8')
            dict = json.loads(data)
            journal = Journal.from_dict(dict)
            # TODO Need to add code to journal/entry models to detect duplicates
            session.add(journal)
            session.commit()
            return redirect(url_for('index'))
        except (JSONDecodeError, TypeError):
            form.errors['upload_error'] = 'Could not parse file, check format'
    return render_template('upload.html', title='Upload data', form=form)

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
