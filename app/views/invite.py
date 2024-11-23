from flask import Blueprint
from flask_login import current_user

from app import User, db
from app.forms import DateProposalForm
from app.models import DateProposal
from app.views.auth import confirmed_required

invite_bp = Blueprint("invite_bp", __name__)


@invite_bp.route("/invite/<int:user_id>", methods=["POST"])
@confirmed_required
def invite(user_id: int):
    form = DateProposalForm()
    # we will also have to validate whether the date is in the future, and whether there are tables available
    # we can probaby write custom wtf validators for that
    if form.validate_on_submit():
        user = db.get_or_404(User, user_id)
        proposal = DateProposal(
            proposer_id=current_user.id, recipient_id=user_id, date=form.date.data, proposal_message=form.message.data
        )
        db.session.add(proposal)
        db.session.commit()
        return "true"
    return form.errors
