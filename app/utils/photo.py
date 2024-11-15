from flask import url_for, current_app


def generate_photo_url(photo) -> str:
    return url_for("static", filename=f"images/{photo.id}.{photo.file_extension}")

def os_photo_url(photo) -> str:
    return f"{current_app.config['UPLOAD_FOLDER']}/{photo.id}.{photo.file_extension}"