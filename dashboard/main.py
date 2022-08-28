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

@main.route('/api/upload', methods=['POST'])
def upload():
    # TODO
    return 'Uploaded successfully'
