from flask import Blueprint, render_template

from app.views.auth import confirmed_required

about_us_page_bp = Blueprint("about_us_page_bp", __name__)


@about_us_page_bp.route("/about-us-page")
@confirmed_required
def about_us_page():
    return render_template("about_us_page.html")
