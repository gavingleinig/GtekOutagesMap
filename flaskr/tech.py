from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('tech', __name__)

@bp.route('/tech', methods=('GET', 'POST'))
@login_required
def tech():
    db = get_db()
    towers = db.execute(
        'SELECT id, longitude, latitude, radius, status FROM towers'
    ).fetchall()
    return render_template('tech.html', towers=towers)