from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort
from datetime import datetime, timedelta, timezone
from GtekOutageMap.auth import login_required
from GtekOutageMap.db import get_db

bp = Blueprint('status', __name__)

def combine_Updates(posts):
    posts_dict = {}
    for post in posts:
        post_id = post['id']
        if post_id not in posts_dict:
            posts_dict[post_id] = {
                'id': post_id,
                'title': post['title'],
                'body': post['body'],
                'status': post['status'],
                'created': post['created'],
                'updates': []
            }
        
        if post['update_id']:
            posts_dict[post_id]['updates'].append({
                'update_id': post['update_id'],
                'update_content': post['update_content'],
                'updated_at': post['updated_at']
            })

    return list(posts_dict.values())

@bp.route('/status', methods=('GET', 'POST'))
def status():
    db = get_db()

    week_cut_off = "0-0-0 0:0:0"
    if not session or session.get('logged_in') != True:
        week_cut_off = (datetime.now(timezone.utc) - timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S')

    print(week_cut_off)

    query = '''
    SELECT 
        p.id, 
        p.title, 
        p.body, 
        p.status, 
        p.created, 
        pu.id AS update_id, 
        pu.update_content, 
        pu.updated_at
    FROM 
        posts p 
    LEFT JOIN 
        post_updates pu 
    ON 
        p.id = pu.post_id
    WHERE 
        p.created >= ?
    ORDER BY 
        p.created DESC, 
        pu.updated_at DESC
'''
    
    
    posts = db.execute(query, (week_cut_off,)).fetchall()

    print(posts)

    posts_list = combine_Updates(posts)
    print(posts_list)

    return render_template('status.html', posts=posts_list)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        status = request.form['status']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO posts (title, body, status)'
                ' VALUES (?, ?, ?)',
                (title, body, status)
            )
            db.commit()
            return redirect(url_for('status.status'))

    return render_template('create.html')

def get_post(id, check_author=True):

    post = get_db().execute(
        '''
        SELECT 
            p.id, 
            p.title, 
            p.body, 
            p.status, 
            p.created, 
            pu.id AS update_id, 
            pu.update_content, 
            pu.updated_at
        FROM 
            posts p 
        LEFT JOIN 
            post_updates pu 
        ON 
            p.id = pu.post_id
        WHERE 
            p.id = ?
        ORDER BY 
            p.created DESC, 
            pu.updated_at DESC
    ''',(id,)
    ).fetchall()

    print(post)
    posts_list = combine_Updates(post)
    post = posts_list[0]

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and not g.user:
        abort(403)

    return post

@bp.route('/<int:id>/edit', methods=('GET', 'POST'))
@login_required
def edit(id):
    post = get_post(id)
    do_update = request.args.get('do_update', 'false').lower() == 'true'

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        status = request.form['status']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE posts SET title = ?, body = ?, status = ? WHERE id = ?',
                (title, body, status, id)
            )

            # Handle updates
            if do_update:
                new_update_text = request.form['new_update_body']
                if new_update_text.strip():  # Check if new update text is not empty
                    db.execute(
                        'INSERT INTO post_updates (post_id, update_content) VALUES (?, ?)',
                        (id, new_update_text)
                    )
                else:
                    # Optionally handle validation or flash message for empty update
                    pass

            # Handle existing updates
            for update in post['updates']:
                update_id = update['update_id']
                update_content = request.form.get(f'update_body_{update_id}', '').strip()
                if update_content:
                    db.execute(
                        'UPDATE post_updates SET update_content = ? WHERE id = ?',
                        (update_content, update_id)
                    )

            db.commit()
            return redirect(url_for('status.status'))

    return render_template('update.html', post=post, do_update=do_update)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM posts WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('status.status'))

@bp.route('/<int:post_id>/update/<int:update_id>', methods=['POST'])
@login_required
def delete_update(post_id, update_id):
    db = get_db()
    db.execute('DELETE FROM post_updates WHERE id = ? AND post_id = ?', (update_id, post_id))
    db.commit()
    return '', 204  # No Content