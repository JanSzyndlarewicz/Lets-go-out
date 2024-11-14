from flask import Blueprint, render_template
from flask_login import login_required

about_us_page_bp = Blueprint("about_us_page_bp", __name__)


@about_us_page_bp.route("/about-us-page")
@login_required
def about_us_page():
    return render_template("about_us_page.html")
