from flask import current_app, url_for


def generate_photo_url(photo) -> str:
    return url_for("static", filename=f"images/{photo.id}.{photo.file_extension}")


def os_photo_url(photo) -> str:
    return f"{current_app.config['UPLOAD_FOLDER']}/{photo.id}.{photo.file_extension}"
