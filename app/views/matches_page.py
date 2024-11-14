from flask import Blueprint, render_template
from flask_login import login_required

matches_page_bp = Blueprint("matches_page_bp", __name__)


@matches_page_bp.route("/matches_page")
@login_required
def matches_page():
    return render_template("matches_page.html")
