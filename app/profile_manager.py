from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user

from sqlalchemy.exc import IntegrityError

from . import db

from .models import available_genders

profile_manager_bp = Blueprint('profile_manager_bp', __name__)

#TODO
#Input validation
#Image uploading
#Consider using wtf or something like that

@profile_manager_bp.route('/profile_manager', methods=['GET', 'POST'])
@login_required
def profile_manager():
    if request.method == 'POST':
        name = request.form.get("name")
        gender = request.form.get("gender")
        description = request.form.get("description")

        gender_preferences = []
        for g in available_genders:
            if request.form.get(g):
                gender_preferences.append(g)

        lower_difference = request.form.get("lower_difference")
        upper_difference = request.form.get("upper_difference")

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

    return render_template('profile_manager.html', genders=available_genders)