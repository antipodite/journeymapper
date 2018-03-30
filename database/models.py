import json

from sqlalchemy import (Column, Integer, String, Date, ForeignKey, 
                        Float, MetaData)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

TIME_FORMAT_STR = '%d %B %Y'

metadata = MetaData()
Base = declarative_base()

class Journal(Base):
    """Represents an explorer's journal"""

    __tablename__ = 'journal'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    source = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)
    author = Column(String)

    entries = relationship('Entry')

    def __init__(self, title, source, start_date, end_date, author, entries=[]):

        # TODO Make most of these optional 
        self.title = title
        self.source = source
        self.start_date = start_date
        self.end_date = end_date
        self.author = author
        self.entries = entries

    def to_json(self, include_entries=False):
        # TODO find a more elegant way to do this.. filter __dict__?
        obj = {'title': self.title,
               'source': self.source,
               'start_date': self.start_date.strftime(TIME_FORMAT_STR),
               'end_date': self.end_date.strftime(TIME_FORMAT_STR),
               'author': self.author}

        if include_entries:
           obj['entries'] = [e.to_dict() for e in self.entries]

        return json.dumps(obj)

    def load_from_json(self):
        """Populate object fields from JSON string
        """
        return 

    def __repr__(self):

        return '<title: {} author: {} #entries: {}>'.format(
            self.title,
            self.author,
            len(self.entries))


class Entry(Base):
    """Represents an entry in the journal"""
    
    __tablename__ = 'entry'

    id = Column(Integer, primary_key=True, autoincrement=True)
    number = Column(Integer)
    date = Column(Date)
    latitude = Column(Float)
    longitude = Column(Float)
    course_bearing = Column(Integer) # TODO Find a way to limit to valid angle
    distance = Column(Float) # In Kilometres
    text = Column(String)

    journal_id = Column(Integer, ForeignKey('journal.id'))
    journal = relationship('Journal', backref='journal_lookup')

    def __init__(self, num, date, lat, lng, bearing, distance, text):
        # TODO Make most of these optional 
        self.number = num
        self.date = date
        self.latitude = lat
        self.longitude = lng
        self.course_bearing = bearing
        self.distance = distance
        self.text = text

    def to_dict(self):
        """Prepare object data for serialization to JSON.

        Filters out all the internal bits and converts non-JSON-able
        types to strings.
        """
        # TODO find a more elegant way to do this.. filter __dict__?
        obj = {'number': self.number,
               'date': self.date.strftime(TIME_FORMAT_STR),
               'latitude': self.latitude,
               'longitude': self.longitude,
               'course_bearing': self.course_bearing,
               'distance': self.distance,
               'text': self.text}

        return obj
 
    def to_json(self):
       return json.dumps(self.to_dict())
    
    def load_from_json(self):
        """Populate object fields from JSON string
        """
        return

    def __repr__(self):
        return '@Entry' # TODO Make this actually informative :)
