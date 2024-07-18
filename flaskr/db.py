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
    
    insert_statements = ""
    with open('flaskr/util/towers.csv', 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)
        
        for row in csvreader:
            name = row['name']
            longitude = float(row['x coordinate'])
            latitude = float(row['y coordinate'])
            radius = int(row['description'])
            status = "active"
            
            insert_statements += f'''
            INSERT INTO towers (name, latitude, longitude, radius, status)
            VALUES ("{name}", {latitude}, {longitude}, {radius}, "{status}");
            '''
    
    db.executescript(insert_statements)


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)