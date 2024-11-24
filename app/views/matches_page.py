from app.views.auth import confirmed_required
from flask import Blueprint, render_template

matches_page_bp = Blueprint("matches_page_bp", __name__)


@matches_page_bp.route("/matches-page")
@confirmed_required
def matches_page():
    return render_template("main/matches_page.html")
