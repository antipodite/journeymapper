#!/usr/bin/env python3
""".
    Simple version of text_analysis.py process. Turns text file of journal
    entries, separated by \n\n, into tabular data and exports it to a TSV
    file.

    Isaac Stead, March 2015
"""
import calendar
import re
import datetime
import sys

from database.models import Journal, Entry

def __float(s):
    """Helper to convert regex string matches to floating point numbers"""

    try:
        return float(s)
    except TypeError:
        return float(0)

def degrees_to_decimal(degrees=0, minutes=0, seconds=0, hemisphere=None):
    """Convert degrees to decimal format"""

    decimal = float(degrees) + float(minutes) / 60 + float(seconds) / 3600
    rounded = round(decimal, 3)
    if hemisphere.upper() in ['N', 'E', 'NORTH', 'EAST', None]:
        return rounded
    if hemisphere.upper() in ['S', 'W', 'SOUTH', 'WEST']:
        return -rounded
    else:
        raise ValueError('{} is not a valid direction'.format(direction))

def find_coordinate_string(text, decimal=False):
    """Search for latitude and longitude readings in specific format"""

    coord_regex = (
        'latitude\s([0-9]+)\sdegree(?:s)?'
        '(\s[0-9]+)?(?:\sminute(?:s)?)?'
        '(\s[0-9]+)?(?:\ssecond(?:s)?)?'
        '\s(North|South)'
        '..'
        '(?:longitude)?\s([0-9]+)\sdegree(?:s)?'
        '(\s[0-9]+)?(?:\sminute(?:s)?)?'
        '(\s[0-9]+)?(?:\ssecond(?:s)?)?'
        '\s(West|East)'
    )
    match = re.search(coord_regex, text, re.IGNORECASE)
    if match:
        elements = match.groups()
        latitude = {'degrees': __float(elements[0]),
                    'minutes': __float(elements[1]),
                    'seconds': __float(elements[2]),
                    'hemisphere': elements[3]}

        longitude = {'degrees': __float(elements[4]),
                     'minutes': __float(elements[5]),
                     'seconds': __float(elements[6]),
                     'hemisphere': elements[7]}

        return {'latitude': latitude, 'longitude': longitude}
    else:
        return None

def extract_date():
    """Get the date string from the beginning of a journal entry.

    We step through the first sentence checking for elements of a date
    entry. Because some elements might be missing in a certain entry,
    we use a closure to keep track of the last value for that element,
    and if that element is not found in this entry, use the last value.
    """

    months = [m.lower() for m in calendar.month_name]
    curr = {} # Values for closure

    def extract(text):
        # Date entry is always before the first period
        date_text = text.split('.')[0]
        # Search for month and day in entry and convert to date object.
        # If no month or year is found, use the last value detected.
        for el in date_text.split():
            if re.match('[0-9]{1,2}', el):
                curr['day'] = int(re.match('[0-9]{1,2}', el).group())
            if el != '' and el.lower() in months:
                curr['month'] = months.index(el.lower())
            if re.match('[0-9]{4}', el):
                curr['year'] = int(re.match('[0-9]{4}', el).group())

        return datetime.date(curr['year'], curr['month'], curr['day'])

    return extract



def parse_journal_text(raw):
    """Process the text of a complete journal
    """
    entries = raw.split('\n\n')
    extractor = extract_date()
    entry_num = 0
    output = []

    for entry in entries:
        entry_num += 1
        date = extractor(entry)
        cs = find_coordinate_string(entry)
        lat = degrees_to_decimal(**cs['latitude']) if cs else None
        lng = degrees_to_decimal(**cs['longitude']) if cs else None
        text = entry
        output.append(Entry(entry_num, date, lat, lng, None, None, text))

    return output 

