from flask import Blueprint, abort, jsonify

from app.models.interest import Interest
from app.views.auth import confirmed_required

# from app.models.database import db

common_bp = Blueprint("common_bp", __name__)

@common_bp.route('/interests')
def interests():
    interests = Interest.query.all()
    if not interests:
        abort(404)
    return jsonify({"interests": [{"id": interest.id, "name": interest.name} for interest in interests]})
