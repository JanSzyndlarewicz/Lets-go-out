from flask import Blueprint, redirect, render_template, url_for
from flask_login import current_user

from app import User, db
from app.views.auth import confirmed_required

profile_bp = Blueprint("profile_bp", __name__)


@profile_bp.route("/profile/<int:user_id>")
@confirmed_required
def profile(user_id):
    user = db.get_or_404(User, user_id)
    if user.id == current_user.id:
        return redirect(url_for("you_page_bp.you_page"))
    return render_template("profile.html", user=user)
