import logging

from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy.exc import IntegrityError

from app import db
from app.forms import ProfileManagerForm
from app.models import Gender

logger = logging.getLogger(__name__)

profile_manager_bp = Blueprint("profile_manager_bp", __name__)

# TODO
# Image uploading and maybe other fields


@profile_manager_bp.route("/profile-manager", methods=["GET", "POST"])
@login_required
def profile_manager():
    form = ProfileManagerForm()

    form.gender_preferences.choices = [(gender.name, gender.value) for gender in Gender]
    form.gender.choices = [(gender.name, gender.value) for gender in Gender]

    if request.method == "GET":
        form.description.data = current_user.profile.description

    if form.validate_on_submit():
        name = form.name.data
        gender = Gender[form.gender.data]
        description = form.description.data.strip()
        lower_difference = form.lower_difference.data
        upper_difference = form.upper_difference.data
        gender_preferences = [Gender[gp] for gp in form.gender_preferences.data]

        logger.info(description)

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
