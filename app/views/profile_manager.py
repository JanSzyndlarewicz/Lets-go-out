from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user

from sqlalchemy.exc import IntegrityError

from .. import db
from ..forms.forms import ProfileManagerForm
from ..models.models import available_genders, available_genders_display

profile_manager_bp = Blueprint("profile_manager_bp", __name__)

# TODO
# Image uploading and maybe other fields


@profile_manager_bp.route("/profile_manager", methods=["GET", "POST"])
@login_required
def profile_manager():
    form = ProfileManagerForm()
    # dynamically pass the list of genders to appropriate inputs
    form.gender_preferences.choices = list(zip(available_genders, available_genders_display))
    form.gender.choices = list(zip(available_genders, available_genders_display))

    # setting some default values that cannot be easily set in jinja
    if request.method == "GET":
        form.description.data = current_user.profile.description

    if form.validate_on_submit():

        name = form.name.data
        gender = form.gender.data
        description = form.description.data.strip()
        lower_difference = form.lower_difference.data
        upper_difference = form.upper_difference.data
        gender_preferences = []
        for g in available_genders:
            if g in form.gender_preferences.data:
                gender_preferences.append(g)

        print(description)

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
            print(e)
        return redirect(url_for("profile_manager_bp.profile_manager"))

    return render_template("profile_manager.html", form=form)
