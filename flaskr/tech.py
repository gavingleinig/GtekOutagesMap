from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)
import sys
import os
from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('tech', __name__)

@bp.route('/tech', methods=('GET', 'POST'))
@login_required
def tech():
    db = get_db()
    towers = db.execute('SELECT name, status, latitude, longitude, radius FROM towers').fetchall()

    if request.method == 'POST':
        action = request.form.get('action')
        selected_towers = request.form.getlist('tower_status[]')

        if action and selected_towers:
            for tower_name in selected_towers:
                new_status = 'online' if action == 'online' else 'offline'
                try:
                    db.execute(
                        "UPDATE towers SET status = ? WHERE name = ?;",
                        (new_status, tower_name)
                    )
                    db.commit()
                except db.IntegrityError:
                    flash("An error occurred while updating the tower status.")

        towers = db.execute('SELECT name, status, latitude, longitude, radius FROM towers').fetchall()

    towers = [dict(row) for row in towers]
    
    google_maps_api_key = os.getenv('GOOGLE_MAPS_API_KEY')
    return render_template('tech.html', towers=towers, google_maps_api_key=google_maps_api_key)

@bp.route('/tech/edit_towers', methods=('GET', 'POST'))
@login_required
def edit_towers():
    db = get_db()
    
    if request.method == 'POST':
        data = request.get_json()
        towers = data.get('towers', [])

        for tower in towers:
            id = tower.get('id')
            name = tower.get('name')
            latitude = tower.get('latitude')
            longitude = tower.get('longitude')
            radius = tower.get('radius')

            # Validate form data
            if not (id and name and latitude and longitude and radius):
                return jsonify({'success': False, 'message': 'All fields are required.'})

            try:
                latitude = float(latitude)
                longitude = float(longitude)
                radius = float(radius)
            except ValueError:
                return jsonify({'success': False, 'message': 'Latitude, Longitude, and Radius must be valid numbers.'})

            try:
                db.execute(
                    'UPDATE towers SET name = ?, latitude = ?, longitude = ?, radius = ? WHERE id = ?',
                    (name, latitude, longitude, radius, id)
                )
                db.commit()
            except db.IntegrityError:
                return jsonify({'success': False, 'message': 'An error occurred while updating the tower.'})

        return jsonify({'success': True, 'message': 'Towers updated successfully!'})

    towers = db.execute('SELECT id, name, status, latitude, longitude, radius FROM towers').fetchall()

    towers = [dict(row) for row in towers]
    
    google_maps_api_key = os.getenv('GOOGLE_MAPS_API_KEY')
    return render_template('edit_towers.html', towers=towers, google_maps_api_key=google_maps_api_key)

@bp.route('/tech/add_tower', methods=('POST',))
@login_required
def add_tower():
    name = request.form['new_name']
    latitude = request.form['new_latitude']
    longitude = request.form['new_longitude']
    radius = request.form['new_radius']
    
    # Validate form data
    if not (name and latitude and longitude and radius):
        flash('All fields are required pt2.', 'error')
        return redirect(url_for('tech.edit_towers'))
    
    try:
        latitude = float(latitude)
        longitude = float(longitude)
        radius = float(radius)
    except ValueError:
        flash('Latitude, Longitude, and Radius must be valid numbers.', 'error')
        return redirect(url_for('tech.edit_towers'))
    
    db = get_db()
    db.execute(
        'INSERT INTO towers (name, latitude, longitude, radius, status) VALUES (?, ?, ?, ?, ?)',
        (name, latitude, longitude, radius, 'online')
    )
    db.commit()
    
    flash('New tower added successfully!', 'success')
    return redirect(url_for('tech.edit_towers'))

@bp.route('/tech/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    db = get_db()
    db.execute('DELETE FROM towers WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('tech.edit_towers'))

def update_tower(tower):
    db = get_db()
    db.execute(
        'UPDATE towers SET name = ?, latitude = ?, longitude = ?, radius = ? WHERE id = ?',
        (tower['name'], tower['latitude'], tower['longitude'], tower['radius'], tower['id'])
    )
    db.commit()