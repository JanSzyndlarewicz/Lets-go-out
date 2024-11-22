from datetime import datetime

from flask import Blueprint, render_template
from flask_login import current_user


from app.forms import DateRequestForm
from app.models.database import db
from app.utils.algorithm import suggest_matches
from app.views.auth import confirmed_required

from app.forms import DateProposalForm


find_page_bp = Blueprint("find_page_bp", __name__)


@find_page_bp.route("/find-page/invite")
@confirmed_required
def find_page_invite():

    date_request_form = DateRequestForm(message_label_text="Optional text attached to accept/reject/reschedule")
    is_requesting = True
    date_request_data = suggest_matches(current_user.id, db.session, 1)[0]
    date_request_data = date_request_data.profile
    return render_template(
        "main/find_page.html", date_request_data=date_request_data, form=date_request_form, is_requesting=is_requesting
    )


@find_page_bp.route("/find-page/answear")
@confirmed_required
def find_page_answear():

    date_request_form = DateRequestForm(
        message_label_text="Optional text attached to accept/reject", given_date=datetime.now().date()
    )
    is_requesting = False
    date_request_data = suggest_matches(current_user.id, db.session, 1)[0]
    date_request_data = date_request_data.profile
    return render_template(
        "main/find_page.html", date_request_data=date_request_data, form=date_request_form, is_requesting=is_requesting
    )
