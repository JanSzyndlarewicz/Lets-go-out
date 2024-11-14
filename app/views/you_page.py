from flask import Blueprint, render_template
from flask_login import login_required

you_page_bp = Blueprint("you_page_bp", __name__)


@you_page_bp.route("/you_page")
@login_required
def you_page():
    return render_template("you_page.html")
