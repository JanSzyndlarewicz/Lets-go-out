from flask import Blueprint, render_template

from flask_login import current_user

from app import db, User

from app.models import DateProposal

from app.views.auth import confirmed_required

from app.forms import DateProposalForm

invite_bp = Blueprint("invite_bp", __name__)


@invite_bp.route("/invite/<int:user_id>", methods=["POST"])
@confirmed_required
def invite(user_id : int):
    form = DateProposalForm()
    if form.validate_on_submit():
        user = db.get_or_404(User, user_id)
        proposal = DateProposal(proposer_id=current_user.id, recipient_id=user_id, date=form.date.data, proposal_message=form.message.data)
        db.session.add(proposal)
        db.session.commit()
        return "true"
    print(form.errors)
    return form.errors
