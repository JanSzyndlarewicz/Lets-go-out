from datetime import datetime

from app.forms import DateRequestForm
from app.models.database import db
from app.utils.algorithm import suggest_matches
from app.views.auth import confirmed_required
from flask import Blueprint, render_template, request
from flask_login import current_user

find_page_bp = Blueprint("find_page_bp", __name__)


@find_page_bp.route("/find-page/invite")
@confirmed_required
def find_page_invite():
    date_request_form = DateRequestForm()
    is_requesting = True

    date_request_data = get_suggested_matches_data(10)
    if not date_request_data:
        date_request_data = None

    return render_template(
        "main/find_page.html",
        date_request_data=date_request_data,
        form=date_request_form,
        is_requesting=is_requesting,
    )


@find_page_bp.route("/find-page/refill", methods=["POST"])
@confirmed_required
def refill():
    ignore_ids = [user["id"] for user in request.json]
    return get_suggested_matches_data(10, ignore_ids=ignore_ids)


def get_suggested_matches_data(limit: int, ignore_ids=None):
    suggested_users = suggest_matches(db.session, current_user.id, limit, ignore_ids)
    result = []
    for user in suggested_users:
        result.append(
            {
                "id": user.id,
                "name": user.profile.name,
                "description": user.profile.description,
            }
        )
    return result


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
        "main/find_page.html",
        date_request_data=date_request_data,
        form=date_request_form,
        is_requesting=is_requesting,
    )
