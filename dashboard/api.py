import os
from flask import Blueprint, current_app, request
from werkzeug.utils import secure_filename
from .models import Video
from . import db

api = Blueprint('api', __name__)

# Define upload API endpoint
@api.route('/api/upload', methods=['POST'])
def upload():
    file = request.files.get('data')
    if not file:
        return 'Error: no data received'

    blob = file.read()
    # search for magic number where metadata are stored
    ofs = blob.rfind(b'w00tw00t')
    if ofs < 0:
        return 'Error: file has no metadata'

    date, kind, loc = blob[ofs + 8:].decode().split(',')
    filename = secure_filename(file.filename)
    new_video = Video(date=date, kind=kind, position=loc, filename=filename)
    db.session.add(new_video)
    db.session.commit()

    # save the file
    save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    with open(save_path, 'wb') as f:
        f.write(blob)

    return 'Upload successful'
