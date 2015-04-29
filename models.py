from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy() # No app parameter to avoid circular import problem

class Entry(db.Model):
    """ A table to store journal entries"""
    __tablename__ = "entries"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    latitude = db.Column(db.Float())
    longitude = db.Column(db.Float())
    text = db.Column(db.Text())

    def __init__(self, date, lat, lng, text):
        self.date = date
        self.latitude = lat
        self.longitude = lng
        self.text = text

    def __repr__(self):
        return '<id:{} date:{} lat:{} lng:{} text:{}>'.format(
            self.id,
            self.date,
            self.latitude,
            self.longitude,
            self.text[32:])
