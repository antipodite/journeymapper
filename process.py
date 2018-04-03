#!/usr/bin/env python3

print(__name__)
import sys
import json
from argparse import ArgumentParser
from database.models import Journal, Entry
from jparser.process_text import parse_journal_text


# Set up the command line interface
parser = ArgumentParser(description='Parse and extract information from'
                                    'a journal and export to JSON file.')
add_argument = parser.add_argument

add_argument('in_file', default=sys.stdin)
add_argument('out_file', default=sys.stdout)
add_argument('--t', type=str, help='Journal title')
add_argument('--s', type=str, help='URL journal text was retrieved from')
add_argument('--a', type=str, help='Author of journal')
args = parser.parse_args()

# Parse journal
with open(args.in_file) as f:
    raw = f.read()

entries = parse_journal_text(raw)
journal = Journal(args.t, args.s, args.a, entries)

with open(args.out_file, 'w+') as f:
    f.write(journal.to_json())

print('I HATE WOMEN')
