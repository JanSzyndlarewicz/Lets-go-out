from app import create_app
from app.models import db, Interests

app = create_app()

with app.app_context():
    db.create_all()

    # Adding default interests
    default_interests = ['Cooking', 'Sports', 'Music', 'Travel', 'Reading', 'Gaming']
    for interest_name in default_interests:
        if not Interests.query.filter_by(name=interest_name).first():
            new_interest = Interests(name=interest_name)
            db.session.add(new_interest)

    db.session.commit()
    print("Default interests added.")
