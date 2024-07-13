import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        #db = get_db()
        error = None
        #user = db.execute(
        #    'SELECT * FROM user WHERE username = ?', (username,)
        #).fetchone()

        #if user is None:
        #    error = 'Incorrect username.'
        #elif not check_password_hash(user['password'], password):
        #    error = 'Incorrect password.'

        if username != "admin":
            error = 'Incorrect username.'
        elif password != "4meonly":
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['logged_in'] = True
            return redirect(url_for('tech.tech'))

        flash(error)

    return render_template('login.html')

# @bp.before_app_request
# def load_logged_in_user():
#     user_id = session.get('logged_in')

#     if user_id is None:
#         g.user = None
#     else:
#         g.user = get_db().execute(
#             'SELECT * FROM user WHERE id = ?', (user_id,)
#         ).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('outage_map'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not session or session['logged_in'] != True:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view