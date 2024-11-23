from flask import Blueprint
from flask_login import current_user

from app import User, db
from app.forms import DateRequestForm, DateProposalForm
from app.models import DateProposal
from app.views.auth import confirmed_required

interaction_bp = Blueprint("interaction_bp", __name__)


@interaction_bp.route("/invite/<int:user_id>", methods=["POST"])
@confirmed_required
def invite(user_id: int):
    form = DateRequestForm()
    # we will also have to validate whether the date is in the future, and whether there are tables available
    # we can probaby write custom wtf validators for that
    print("invite")
    if form.validate_on_submit():
        print("przeszło")
        user = db.get_or_404(User, user_id)
        proposal = DateProposal(
            proposer_id=current_user.id, recipient_id=user_id, date=form.date.data, proposal_message=form.message.data
        )
        db.session.add(proposal)
        db.session.commit()
        return "true"
    print("nie przeszło")
    print(form.errors)
    return form.errors


@interaction_bp.route("/reject/<int:user_id>", methods=["POST"])
@confirmed_required
def reject(user_id: int):
    user = db.get_or_404(User, user_id)
    current_user.rejected.append(user)
    user.rejecters.append(current_user)
    db.session.commit()
    return "true"

