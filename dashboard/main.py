from flask import Blueprint, render_template, redirect, url_for, request
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

@main.route('/dashboard/notifications')
@login_required
def notifications():
    user = User.query.filter_by(name=current_user.name).first()
    return render_template('notification.html', email=user.email, notify=user.notify)

@main.route('/dashboard/notifications', methods=['POST'])
@login_required
def notifications_update():
    enabled = request.form.get('enabled')
    email = request.form.get('email')
    # update user preferences
    user = User.query.filter_by(name=current_user.name).first()
    user.email = email
    user.notify = True if enabled else False
    # save to database
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('main.notifications'))


# Define upload API endpoint
@main.route('/api/upload', methods=['POST'])
def upload():
    # TODO
    return 'Uploaded successfully'
