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
        'SELECT name, status FROM towers'
    ).fetchall()


    if request.method == 'POST':

        try:
            db.execute(
                "UPDATE towers SET status = 'Online';"
            )
            db.commit()
        except db.IntegrityError:
            flash(error)

        selected_towers = request.form.getlist('tower_status[]')
        towers_to_update = [tower for tower in towers if tower['name'] in selected_towers]
        
        for tower in towers_to_update:
            try:
                db.execute(
                    "UPDATE towers SET status = 'Offline' WHERE name = ?;",
                    (tower['name'],)
                )
                db.commit()
            except db.IntegrityError:
                flash(error)
        
        towers = db.execute(
        'SELECT name, status FROM towers'
        ).fetchall()

    
    return render_template('tech.html', towers=towers)
