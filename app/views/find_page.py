from flask import Blueprint, render_template
from flask_login import login_required

find_page_bp = Blueprint("find_page_bp", __name__)


@find_page_bp.route("/find_page")
@login_required
def find_page():
    return render_template("find_page.html")
