from datetime import datetime

from flask import Blueprint, request
from flask_login import current_user

from app import User, db
from app.forms import DateRequestForm
from app.models import DateProposal, ProposalStatus
from app.views.auth import confirmed_required

interaction_bp = Blueprint("interaction_bp", __name__)

@interaction_bp.route("/like/<int:user_id>", methods=["POST"])
@confirmed_required
def like(user_id):
    if user_id != current_user.id:
        user = db.get_or_404(User, user_id)
        if current_user in user.likers:
            user.likers.remove(current_user)
            db.session.commit()
        else:
            user.likers.append(current_user)
            db.session.commit()
        return "", 200
    return "", 400

@interaction_bp.route("/block/<int:user_id>", methods=["POST"])
@confirmed_required
def block(user_id):
    if user_id != current_user.id:
        user = db.get_or_404(User, user_id)
        if current_user in user.blockers:
            user.blockers.remove(current_user)
        else:
            user.blockers.append(current_user)
        db.session.commit()
        return "", 200
    return "", 400

@interaction_bp.route("/invite", methods=["POST"])
@confirmed_required
def invite():
    form = DateRequestForm()
    # we will also have to validate whether there are tables available
    if form.validate_on_submit():
        user = db.get_or_404(User, form.id.data)
        proposal = DateProposal(
            proposer_id=current_user.id,
            recipient_id=form.id.data,
            date=form.date.data,
            proposal_message=form.message.data,
        )
        if user in current_user.blockers:
            proposal.status = ProposalStatus.ignored
        db.session.add(proposal)
        db.session.commit()
        return "", 200
    return form.errors, 400


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
        return "", 200
    return form.errors, 400

@interaction_bp.route("/accept", methods=["POST"])
@confirmed_required
def accept():
    form = DateRequestForm()
    if form.validate_on_submit():
        proposal = db.get_or_404(DateProposal, form.id.data)
        if proposal.recipient_id == current_user.id:
            proposal.change_status(ProposalStatus.accepted, form.message.data)
            db.session.commit()
            return "", 200
        return "", 401
    return form.errors, 400

@interaction_bp.route("/reject-invitation", methods=["POST"])
@confirmed_required
def reject_invitation():
    form = DateRequestForm()
    if form.validate_on_submit():
        proposal = db.get_or_404(DateProposal, form.id.data)
        if proposal.recipient_id == current_user.id:
            proposal.change_status(ProposalStatus.rejected, form.message.data)
            db.session.commit()
            return "", 200
        return "", 401
    return form.errors, 400

@interaction_bp.route("/ignore", methods=["POST"])
@confirmed_required
def ignore():
    form = DateRequestForm()
    del form.message
    if form.validate_on_submit():
        proposal = db.get_or_404(DateProposal, form.id.data)
        if proposal.recipient_id == current_user.id:
            proposal.change_status(ProposalStatus.ignored)
            db.session.commit()
            return "", 200
        return "", 401
    return form.errors, 400

@interaction_bp.route("/reschedule", methods=["POST"])
@confirmed_required
def reschedule():
    form = DateRequestForm()
    if form.validate_on_submit():
        proposal = db.get_or_404(DateProposal, form.id.data)
        if proposal.recipient_id == current_user.id:
            proposal.change_status(ProposalStatus.reschedule, form.message.data)
            db.session.commit()
            return "", 200
        return "", 401
    return form.errors, 400