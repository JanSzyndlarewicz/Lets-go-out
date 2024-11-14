from flask import Blueprint, render_template
from flask_login import login_required

from .. import db, User

profile_bp = Blueprint("profile_bp", __name__)


@profile_bp.route("/profile/<int:user_id>")
@login_required
def profile(user_id):
    user = db.get_or_404(User, user_id)
    return render_template("profile.html", user=user)
