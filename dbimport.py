#! /usr/bin/env python3
'''
    Import journal data from a JSON file into specified SQLite database
'''
# TODO Add check for whether tables exist, create them if they don't
# TODO Add option to wipe DB
# TODO Add check for whether journal exists in DB

import json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from argparse import ArgumentParser

from database.models import Journal, Entry, Metadata

def main():
    # Set up CLI
    parser = ArgumentParser(description='Load a JSON file containing journal data'
                                        'and store it in given database.')
    add_argument = parser.add_argument
    add_argument('json_file')
    add_argument('db_file')
    args = parser.parse_args()

    # Load journal text, parse and build objects
    with open(args.json_file, 'r') as f:
        data = json.loads(f.read())
    journal = Journal.from_dict(data)

    # Connect to DB, create tables if blank, and save objects
    engine = create_engine('sqlite:///' + args.db_file)
    Metadata.create_all(bind=engine)
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    session.add(journal)
    session.commit()
    session.close()

if __name__ == '__main__':
    main()


