import datetime

from app import db
from app.models import RejectedAssociation


def delete_rejects(app):
    with app.app_context():
        current_date = datetime.datetime.today()
        delta = datetime.timedelta(days=app.config["REJECT_DAYS_DURATION"])
        cutoff_date = current_date - delta
        rejects = RejectedAssociation.query.filter(RejectedAssociation.created_date <= cutoff_date).all()
        for reject in rejects:
            db.session.delete(reject)
        db.session.commit()