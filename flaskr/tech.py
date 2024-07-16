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



@bp.route('/tech/edit_towers', methods=('GET', 'POST'))
@login_required
def edit_towers():
    if request.method == 'POST':
        # Process form data
        towers = []
        for i in range(1, len(request.form) // 4 + 1):
            tower_data = {
                'name': request.form.get(f'name_{i}'),
                'latitude': request.form.get(f'latitude_{i}'),
                'longitude': request.form.get(f'longitude_{i}'),
                'radius': request.form.get(f'radius_{i}')
            }
            towers.append(tower_data)
        
        # Perform the update operation in your database
        for tower in towers:
            # Assuming you have a function to update tower data
            update_tower(tower)
        
        flash('Towers updated successfully!', 'success')
        return redirect(url_for('tech.edit_towers'))
    
    db = get_db()
    towers = db.execute('SELECT id, name, latitude, longitude, radius FROM towers').fetchall()
    
    return render_template('edit_towers.html', towers=towers)

def update_tower(tower):
    # Replace with your logic to update a tower in the database
    pass

@bp.route('/tech/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    db = get_db()
    db.execute('DELETE FROM towers WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('tech.edit_towers'))