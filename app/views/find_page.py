from datetime import datetime

from flask import Blueprint, render_template
from flask_login import current_user

from app.forms import DateRequestForm
from app.models.database import db
from app.utils.algorithm import suggest_matches
from app.views.auth import confirmed_required

find_page_bp = Blueprint("find_page_bp", __name__)


@find_page_bp.route("/find-page/invite")
@confirmed_required
def find_page_invite():
    date_request_data = suggest_matches(db.session, current_user.id, 1)
    if not date_request_data:
        return render_template("main/find_page.html", date_request_data=None)

    date_request_form = DateRequestForm()
    is_requesting = True
    date_request_data = date_request_data[0].profile
    return render_template(
        "main/find_page.html", date_request_data=date_request_data, form=date_request_form, is_requesting=is_requesting
    )


@find_page_bp.route("/find-page/answear")
@confirmed_required
def find_page_answear():
    date_request_data = suggest_matches(db.session, current_user.id, 1)
    if not date_request_data:
        return render_template("main/find_page.html", date_request_data=None)

    date_request_form = DateRequestForm(given_date=datetime.now().date())
    is_requesting = False
    date_request_data = date_request_data[0].profile
    return render_template(
        "main/find_page.html", date_request_data=date_request_data, form=date_request_form, is_requesting=is_requesting
    )
