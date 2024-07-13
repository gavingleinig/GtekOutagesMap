from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('outage_map', __name__)

@bp.route('/')
def index():
    return render_template('outage_map.html')


@bp.route('/data')
def data():
    db = get_db()
    towers = db.execute(
        'SELECT name, longitude, latitude, radius, status FROM towers'
    ).fetchall()

    towers_list = [
        dict(name=row['name'], longitude=row['longitude'], latitude=row['latitude'], radius=row['radius'], status=row['status'])
        for row in towers
    ]
    
    return jsonify({'towers': towers_list})
