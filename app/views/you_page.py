from app.views.auth import confirmed_required
from flask import Blueprint, render_template

you_page_bp = Blueprint("you_page_bp", __name__)


@you_page_bp.route("/you-page")
@confirmed_required
def you_page():
    return render_template("main/you_page.html")
