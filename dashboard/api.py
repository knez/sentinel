import os
import hashlib
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

    signature = request.headers.get('Signature')
    if not signature:
        return 'Error: file is not signed'

    blob = file.read()
    if not verify_signature(blob, signature):
        return 'Error: signature verification failed'

    # search for magic number where metadata are stored
    ofs = blob.rfind(b'w00tw00t')
    if ofs < 0:
        return 'Error: file has no metadata'

    metadata = blob[ofs + 8:].decode().split(',')
    save_db(metadata, file.filename)
    save_file(blob, file.filename)

    return 'Upload successful'


def verify_signature(blob, signature):
    secret_key = current_app.config['SECRET_KEY'].encode()
    sha256 = hashlib.sha256(secret_key + blob)
    return sha256.hexdigest() == signature

def save_db(metadata, filename,):
    safe_name = secure_filename(filename)
    date, kind, pos = metadata
    new_video = Video(date=date, kind=kind, position=pos, filename=safe_name)
    db.session.add(new_video)
    db.session.commit()

def save_file(blob, filename):
    save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    with open(save_path, 'wb') as f:
        f.write(blob)
