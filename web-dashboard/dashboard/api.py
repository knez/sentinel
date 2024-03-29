import os
import hashlib
from flask import Blueprint, current_app, request, Response
from flask_login import current_user
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
from .models import User, Video
from . import db

api = Blueprint('api', __name__)

# Define upload API endpoint
@api.route('/api/upload', methods=['POST'])
def upload():
    file = request.files.get('data')
    if not file:
        return Response('No data received', status=400)

    signature = request.headers.get('Signature')
    if not signature:
        return Response('File is not signed', status=400)

    blob = file.read()
    if not verify_signature(blob, signature):
        return Response('Signature verification failed', status=403)

    # search for magic number where metadata are stored
    ofs = blob.rfind(b'w00tw00t')
    if ofs < 0:
        return 'Error: file has no metadata'

    metadata = blob[ofs + 8:].decode().split(',')
    save_db(metadata, file.filename)
    save_file(blob, file.filename)

    # send email notification if enabled
    notify(metadata)

    return Response('Upload successful', status=200)


def verify_signature(blob, signature):
    secret_key = current_app.config['SECRET_KEY'].encode()
    sha256 = hashlib.sha256(secret_key + blob)
    return sha256.hexdigest() == signature

def save_db(metadata, filename,):
    safe_name = secure_filename(filename)
    date, time, kind, pos = metadata
    new_video = Video(date=date, time=time, kind=kind, position=pos, filename=safe_name)
    db.session.add(new_video)
    db.session.commit()

def save_file(blob, filename):
    save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    with open(save_path, 'wb') as f:
        f.write(blob)

def notify(metadata):
    date, time, kind, pos = metadata
    user = User.query.get(1)
    if user.notify:
        mail = Mail(current_app)
        msg = Message('Intruder detected!',  sender ='sentinel@localhost', recipients=[user.email])
        msg.body = f"On {date} sentinel detected an object of type {kind} at location {pos}.\n"
        msg.body += "For full video footage, visit http://localhost:8080"
        mail.send(msg)
