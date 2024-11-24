from app import User, db
from app.forms import DateProposalForm, DateRequestForm
from app.models import DateProposal
from app.views.auth import confirmed_required
from flask import Blueprint, request
from flask_login import current_user

interaction_bp = Blueprint("interaction_bp", __name__)


@interaction_bp.route("/invite", methods=["POST"])
@confirmed_required
def invite():
    form = DateRequestForm()
    # we will also have to validate whether the date is in the future, and whether there are tables available
    # we can probaby write custom wtf validators for that
    if form.validate_on_submit():
        db.get_or_404(User, form.id.data)
        proposal = DateProposal(
            proposer_id=current_user.id,
            recipient_id=form.id.data,
            date=form.date.data,
            proposal_message=form.message.data,
        )
        db.session.add(proposal)
        db.session.commit()
        return "true"
    return form.errors


@interaction_bp.route("/reject", methods=["POST"])
@confirmed_required
def reject():
    form = DateRequestForm()
    del form.message
    del form.date
    if form.validate_on_submit():
        user = db.get_or_404(User, form.id.data)
        current_user.rejected.append(user)
        db.session.commit()
        return "true"
    return "false"
