from flask import Blueprint, render_template

from app.forms import DateRequestForm
from app.views.auth import confirmed_required

find_page_bp = Blueprint("find_page_bp", __name__)


@find_page_bp.route("/find-page")
@confirmed_required
def find_page():
    date_request_form = DateRequestForm(
        message_label_text="Optional text attached to accept/reject/reschedule", given_date="2021-01-01"
    )
    is_requesting = True
    return render_template("main/find_page.html", form=date_request_form, is_requesting=is_requesting)
