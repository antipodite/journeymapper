"""
    Import data from csv file to the local database
"""
import csv
import sys
from app import db, Entry
from datetime import datetime

csvfile= sys.argv[1]

with open(csvfile, 'r') as f:
    # Remove previous rows
    db.session.query(Entry).delete()
    reader = csv.reader(f)
    rows = [row for row in reader]
    number = 1

    for row in rows:
        number += 1
        date = datetime.strptime(row[0], '%Y-%m-%d')
        lat = row[1] if row[1] != '' else None
        lng = row[2] if row[2] != '' else None
        text = row[3] if row[3] != '' else None
        e = Entry(number=number, date=date, lat=lat, lng=lng, text=text)
        db.session.add(e)
    db.session.commit()
