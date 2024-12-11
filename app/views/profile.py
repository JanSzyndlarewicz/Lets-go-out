from flask import Blueprint, redirect, render_template, url_for
from flask_login import current_user

from app import User, db
from app.forms.date_request_form import DateRequestForm
from app.views.auth import confirmed_required

profile_bp = Blueprint("profile_bp", __name__)


@profile_bp.route("/profile/<int:user_id>")
@confirmed_required
def profile(user_id):
    date_request_form = DateRequestForm(message_label_text="Optional text attached to invite/reject")
    user = db.get_or_404(User, user_id)
    if user.id == current_user.id:
        return redirect(url_for("you_page_bp.you_page"))
    # if date_request_form.validate_on_submit():
        
    return render_template("profile.html", user=user, form=date_request_form)
