import logging
import os

from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user
from sqlalchemy.exc import IntegrityError
from werkzeug.utils import secure_filename

from app import db
from app.forms import ProfileManagerForm
from app.models import Gender, Photo
from app.views.auth import confirmed_required

logger = logging.getLogger(__name__)

profile_manager_bp = Blueprint("profile_manager_bp", __name__)


@profile_manager_bp.route("/profile-manager", methods=["GET", "POST"])
@confirmed_required
def profile_manager():
    form = ProfileManagerForm()

    form.gender_preferences.choices = [(gender.name, gender.value) for gender in Gender]
    form.gender.choices = [(gender.name, gender.value) for gender in Gender]

    if request.method == "GET":
        form.description.data = current_user.profile.description
        photo_url = None
        if current_user.profile.photo:
            photo_url = current_user.profile.photo.flask_photo_url
        return render_template("profile_manager.html", form=form, photo_url=photo_url)

    if form.validate_on_submit():
        name = form.name.data
        gender = Gender[form.gender.data]
        description = form.description.data.strip()
        lower_difference = form.lower_difference.data
        upper_difference = form.upper_difference.data
        gender_preferences = [Gender[gp] for gp in form.gender_preferences.data]

        if form.photo.data:
            photo = form.photo.data
            handle_photo_upload(photo, current_user)

        current_user.profile.name = name
        current_user.profile.gender = gender
        current_user.profile.description = description
        current_user.matching_preferences.gender_preferences = gender_preferences
        current_user.matching_preferences.lower_difference = lower_difference
        current_user.matching_preferences.upper_difference = upper_difference

        try:
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            logger.error(e)
        return redirect(url_for("profile_manager_bp.profile_manager"))

    return render_template("profile_manager.html", form=form)


def handle_photo_upload(photo, user) -> Photo:
    if user.profile.photo:
        old_photo_path = user.profile.photo.os_photo_url
        if os.path.exists(old_photo_path):
            os.remove(old_photo_path)
        else:
            logger.error(f"Photo path {old_photo_path} does not exist")

        db.session.delete(user.profile.photo)

    extension = secure_filename(photo.filename).split(".")[-1]
    new_photo = Photo(profile=user.profile, file_extension=extension)

    db.session.add(new_photo)
    db.session.commit()

    photo.save(new_photo.os_photo_url)

    user.profile.photo = new_photo

    return new_photo
