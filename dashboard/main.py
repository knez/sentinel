from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return redirect(url_for('main.dashboard'))

@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.name)

@main.route('/dashboard/notifications')
@login_required
def notifications():
    return render_template('notification.html', name=current_user.name)


# Define API endpoints
@main.route('/api/update', methods=['POST'])
def update():
    # TODO
    return ''

@main.route('/api/delete')
def delete():
    # TODO
    return ''

@main.route('/api/upload', methods=['POST'])
def upload():
    # TODO
    return 'Uploaded successfully'
