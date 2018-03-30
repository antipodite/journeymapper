from sqlalchemy import (Column, Integer, String, Date, ForeignKey, 
                        Float, MetaData)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

metadata = MetaData()
Base = declarative_base(metadata=metadata)

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

        self.title = title
        self.source = source
        self.start_date = start_date
        self.end_date = end_date
        self.author = author
        self.entries = entries

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

    def __repr__(self):
        return '@Entry' # TODO Make this actually informative :)
