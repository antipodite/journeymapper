from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy() # No app parameter to avoid circular import problem

class Journal(db.Model):
    """Represents a journal. A journal has many entries."""
    __tablename__ = "journals"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text())
    author = db.Column(db.Text())
    entries = db.relationship("Entry", backref="journals")

    def __init__(self, title, author, entries=[]):
        self.title = title
        self.author = author
        self.entries = entries

    def __repr__(self):
        return "<title:{} author:{} num_entries: {}".format(
            self.title,
            self.author,
            len(self.entries))

class Entry(db.Model):
    """ A table to store journal entries"""
    __tablename__ = "entries"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    latitude = db.Column(db.Float())
    longitude = db.Column(db.Float())
    text = db.Column(db.Text())
    journal_id = db.Column(db.Integer, db.ForeignKey("journals.id"))

    def __init__(self, date, lat, lng, text):
        self.date = date
        self.latitude = lat
        self.longitude = lng
        self.text = text

    def to_json(self):
        """Return a dictionary representation of the object, for use
        with JSON reponses."""
        # Datetime.strftime doesn't work with years before 1900
        obj = {'date': self.date.isoformat(),
               'lat': self.latitude,
               'lng': self.longitude,
               'text': self.text}
        return obj

    def to_latlng(self):
        """Return the position of the entry as a Gmaps LatLng literal
        JSON, or None if it has no position"""
        obj = {'lat': self.latitude,
               'lng': self.longitude}
        return obj

    def __repr__(self):
        return '<id:{} date:{} lat:{} lng:{} text:{}>'.format(
            self.id,
            self.date,
            self.latitude,
            self.longitude,
            self.text[32:])
