from datetime import datetime

from flask import current_app as app
from flask import Blueprint, redirect, render_template, request, url_for

from flask_login import current_user

from app.forms import DateRequestForm
from app.models import DateProposal, ProposalStatus
from app.models.database import db
from app.utils.algorithm import suggest_matches
from app.views.auth import confirmed_required

find_page_bp = Blueprint("find_page_bp", __name__)


@find_page_bp.route("/find-page/")
@confirmed_required
def find_page():
    return redirect(url_for("find_page_bp.find_page_invite"))

@find_page_bp.route("/find-page/invite")
@confirmed_required
def find_page_invite():
    date_request_form = DateRequestForm()
    is_requesting = True

    date_request_data = get_suggested_matches_data(app.config["INITIAL_SUGGESTION_NUMBER"])
    if not date_request_data:
        date_request_data = None
    
    return render_template(
        "main/find_page.html",
        date_request_data=date_request_data,
        form=date_request_form,
        is_requesting=is_requesting,
        redirect_buttons_set_data=redirect_buttons_set_data(),
        active_nav="find"
    )


@find_page_bp.route("/find-page/refill", methods=["POST"])
@confirmed_required
def refill():
    ignore_ids = [user["id"] for user in request.json]
    return get_suggested_matches_data(app.config["REFILL_SUGGESTION_NUMBER"], ignore_ids=ignore_ids)


def get_suggested_matches_data(limit: int, ignore_ids=[]) -> list[dict]:
    suggested_users = suggest_matches(db.session, current_user.id, limit, ignore_ids)
    result = []
    for user in suggested_users:
        result.append(
            {
                "id": user.id,
                "name": user.profile.name,
                "description": user.profile.description,
                "image_url": user.profile.profile_picture_url_or_default
            }
        )
    return result


@find_page_bp.route("/find-page/answear")
@confirmed_required
def find_page_answear():
    date_request_form = DateRequestForm()

    date_request_data = get_pending_invitations_data(current_user.id)
    is_requesting = False

    if not date_request_data:
        date_request_data = None

    return render_template(
        "main/find_page.html",
        date_request_data=date_request_data,
        form=date_request_form,
        is_requesting=is_requesting,
        redirect_buttons_set_data=redirect_buttons_set_data(),
        active_nav="find"
    )

def get_pending_invitations(user_id : int) -> list[DateProposal]:
    query = (db.select(DateProposal)
             .where(DateProposal.recipient_id == user_id)
             .where(DateProposal.date >= datetime.now().date())
             .where(DateProposal.status == ProposalStatus.proposed)
             .where(~DateProposal.proposer_id.in_(user.id for user in current_user.blocking))
            )
    return db.session.execute(query).scalars().all()

def get_pending_invitations_data(user_id):
    invitations = get_pending_invitations(user_id)
    result = []
    for invitation in invitations:
        result.append(
            {
                "id": invitation.id,
                "name": invitation.proposer.profile.name,
                "description": invitation.proposer.profile.description,
                "message" : invitation.proposal_message, #"" if invitation.proposal_message is None else invitation.proposal_message,
                "date" : invitation.date.strftime(r"%Y-%m-%d")
            }
        )
    return result    

def redirect_buttons_set_data():
    return [{"url": url_for("find_page_bp.find_page_answear"), "text": "answear"}, {"url": url_for("find_page_bp.find_page_invite"), "text": "invite"}]