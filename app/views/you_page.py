from flask import Blueprint, render_template

from app.views.auth import confirmed_required

you_page_bp = Blueprint("you_page_bp", __name__)


@you_page_bp.route("/you-page")
@confirmed_required
def you_page():
    return render_template("base/you_page.html")
