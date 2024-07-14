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
    towers = db.execute('SELECT name, status FROM towers').fetchall()

    if request.method == 'POST':
        action = request.form.get('action')
        selected_towers = request.form.getlist('tower_status[]')

        if action and selected_towers:
            for tower_name in selected_towers:
                new_status = 'Online' if action == 'online' else 'Offline'
                try:
                    db.execute(
                        "UPDATE towers SET status = ? WHERE name = ?;",
                        (new_status, tower_name)
                    )
                    db.commit()
                except db.IntegrityError:
                    flash("An error occurred while updating the tower status.")

        towers = db.execute('SELECT name, status FROM towers').fetchall()

    return render_template('tech.html', towers=towers)