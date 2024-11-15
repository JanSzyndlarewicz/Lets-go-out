from flask import url_for

def generate_photo_url(photo):
    return url_for('static', filename=f"images/{photo.id}.{photo.file_extension}")