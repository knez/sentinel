import os
from flask import Blueprint, render_template, flash, redirect, url_for, request, current_app
from flask_login import login_required, current_user
from .models import User, Video
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return redirect(url_for('main.dashboard'))

@main.route('/dashboard')
@login_required
def dashboard():
    videos = Video.query.all()
    return render_template('dashboard.html', videos=videos)


@main.route('/dashboard/notifications', methods=['GET', 'POST'])
@login_required
def notifications_update():
    user = User.query.filter_by(name=current_user.name).first()
    if request.method == 'GET':
        return render_template('notification.html', email=user.email, notify=user.notify)
    else:
        # POST request, update user preferences
        user.email = request.form.get('email')
        user.notify = True if request.form.get('enabled') else False
        # save to database
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('main.notifications_update'))


@main.route('/dashboard/delete/<int:id>')
@login_required
def delete(id):
    filename = Video.query.get(id).filename
    Video.query.filter(id==id).delete()
    db.session.commit()
    save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    os.unlink(save_path)
    return redirect(url_for('main.dashboard'))
