from datetime import datetime

from sqlalchemy import (Column, Integer, String, Date, ForeignKey, 
                        Float, MetaData)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

TIME_FORMAT_STR = '%d %B %Y'

Base = declarative_base()
metadata = Base.metadata

class Journal(Base):
    '''Represents an explorer's journal'''

    __tablename__ = 'journal'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    source = Column(String)
    author = Column(String)

    entries = relationship('Entry')

    def __init__(self, title, source, author, entries=[]):

        self.title = title
        self.source = source
        self.author = author
        self.entries = entries

    def to_dict(self, include_entries=True):
        '''
        Serialize object data to a dict to be stored as JSON,
        handling type conversion as necessary.
        '''
        data = {'title': self.title, 
                'source': self.source, 
                'author': self.author}

        if include_entries:
           data['entries'] = [e.to_dict() for e in self.entries]

        return data

    @classmethod
    def from_dict(cls, data):
        '''
        Return a new instance with data loaded from a dict read from
        JSON journal format, handling type conversion as necessary.
        '''
        for k, v in data.items():
            if k == 'entries':
                data[k] = [Entry.from_dict(e) for e in v]

        return cls(**data)
        
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

    # TODO num, date fields mandatory in DB and constructor
    def __init__(self, number, date, latitude, longitude, 
                 course_bearing, distance, text):
        self.number = number
        self.date = date
        self.latitude = latitude
        self.longitude = longitude
        self.course_bearing = course_bearing
        self.distance = distance
        self.text = text

    def to_dict(self):
        '''
        Prepare object data for serialization to JSON.

        Filters out all the internal bits and converts non-JSON-able
        types to strings.
        '''
        # TODO find a more elegant way to do this.. filter __dict__?
        obj = {'number': self.number,
               'date': self.date.strftime(TIME_FORMAT_STR),
               'latitude': self.latitude,
               'longitude': self.longitude,
               'course_bearing': self.course_bearing,
               'distance': self.distance,
               'text': self.text}

        return obj
    
    @classmethod
    def from_dict(cls, data):
        '''
        Return a new instance with data loaded from a dict read from
        JSON journal format, handling type conversion as necessary.
        '''
        for k, v in data.items():
            if k == 'date':
                data[k] = datetime.strptime(v, TIME_FORMAT_STR)

        return cls(**data)

    def __repr__(self):
        return '@Entry' # TODO Make this actually informative :)
