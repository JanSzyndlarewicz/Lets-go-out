from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user

from sqlalchemy.exc import IntegrityError

from . import db

from .models import Gender

profile_manager_bp = Blueprint('profile_manager_bp', __name__)

@profile_manager_bp.route('/profile_manager', methods=['GET', 'POST'])
@login_required
def profile_manager():
    if request.method == 'POST':
        name = request.form.get("name")
        gender = request.form.get("gender")
        description = request.form.get("description")
        
        print(gender)

        current_user.profile.name = name
        current_user.profile.gender = gender
        current_user.profile.description = description

        print(current_user.profile.gender)

        try:
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            print(e)
        return redirect(url_for("profile_manager_bp.profile_manager"))

    print([g.value for g in Gender])
    return render_template('profile_manager.html', genders=[g.value for g in Gender])