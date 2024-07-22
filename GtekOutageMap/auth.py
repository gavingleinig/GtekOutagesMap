import functools
import json
import os
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash




bp = Blueprint('auth', __name__)



# Load credentials from file
def load_credentials():
    with open(os.getenv('CREDENTIALS_FILE', 'credentials.json')) as f:
        return json.load(f)



@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        credentials = load_credentials()
        user = credentials.get(username)

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['logged_in'] = True
            return redirect(url_for('tech.tech'))

        flash(error)

    return render_template('login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('logged_in')

    if user_id is None:
        g.user = None
    else:
        g.user = "admin"

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('outage_map.map'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not session or session.get('logged_in') != True:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view