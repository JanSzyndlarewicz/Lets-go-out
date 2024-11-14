from flask import Blueprint, redirect, render_template, url_for
from flask_login import current_user
from sqlalchemy.exc import IntegrityError

from app import db
from app.forms import AccountManagerForm
from app.views.auth import confirmed_required

account_manager_bp = Blueprint("account_manager_bp", __name__)


@account_manager_bp.route("/account-manager", methods=["GET", "POST"])
@confirmed_required
def account_manager():

    form = AccountManagerForm()

    if form.validate_on_submit():
        if current_user.check_password(form.old_password.data):
            current_user.set_password(form.new_password.data)

            try:
                db.session.commit()
            except IntegrityError as e:
                db.session.rollback()
                print(e)
        else:
            return "Invalid credentials", 401
        return redirect(url_for("find_page_bp.find_page"))

    return render_template("account_manager.html", form=form)
