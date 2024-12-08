import datetime

from app import create_app, db
from app.models import RejectedAssociation

from flask_apscheduler import APScheduler


app = create_app()
app.scheduler = APScheduler()

@app.scheduler.task('interval', id='my_job', days=1)
def delete_rejects():
    with app.app_context():
        current_date = datetime.datetime.today()
        delta = datetime.timedelta(days=app.config["REJECT_DAYS_DURATION"])
        cutoff_date = current_date - delta
        rejects = RejectedAssociation.query.filter(RejectedAssociation.created_date <= cutoff_date).all()
        for reject in rejects:
            db.session.delete(reject)
        db.session.commit()

if __name__ == "__main__":
    app.scheduler.init_app(app)
    app.scheduler.start()
    app.run(debug=True)

