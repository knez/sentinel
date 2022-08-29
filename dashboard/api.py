from flask import Blueprint
from .models import Video
from . import db

api = Blueprint('api', __name__)

# Define upload API endpoint
@api.route('/api/upload')
def upload():
    # TODO
    return 'Uploaded successfully'
