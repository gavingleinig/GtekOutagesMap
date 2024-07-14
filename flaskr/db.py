import sqlite3

import click
from flask import current_app, g
import csv


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))
    
    # INSERT INTO towers (name, latitude, longitude, radius, status) VALUES ("Patrick Farms GE",27.6701583531,-97.9140368697,4,"active");
    # INSERT INTO towers (name, latitude, longitude, radius, status) VALUES ("Alice Fire Department",27.7533776428,-98.0707372187,10,"active");
    # with open('towers.csv', 'r') as csvfile:
    #     csvreader = csv.DictReader(csvfile)
        
    #     for row in csvreader:
    #         name = row['name']
    #         longitude = float(row['x coordinate'])
    #         latitude = float(row['y coordinate'])
    #         radius = int(row['description'])
    #         status = "active"
            
    #         # Insert data into the SQLite table
    #         cursor.execute('''
    #         INSERT INTO towers (name, latitude, longitude, radius, status)
    #         VALUES (?, ?, ?, ?, ?)
    #         ''', (name, latitude, longitude, radius, status))


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)