from app import create_app
<<<<<<< HEAD

from sqlalchemy.exc import IntegrityError

from werkzeug.security import generate_password_hash

from app.models import db, User
=======
from app.models import db, Interests
>>>>>>> e6010eba14b91dd79d2b3c1ba5cd011cb8055512

app = create_app()

with app.app_context():
    db.create_all()

    # Adding default interests
    default_interests = ['Cooking', 'Sports', 'Music', 'Travel', 'Reading', 'Gaming']
    for interest_name in default_interests:
        if not Interests.query.filter_by(name=interest_name).first():
            new_interest = Interests(name=interest_name)
            db.session.add(new_interest)

<<<<<<< HEAD
    username = 'admin'
    password = 'admin'  # Hash this in production
    email = 'admin'

    password_hash = generate_password_hash(password)

    existing_user = User.query.filter_by(username=username).first()
    if existing_user is None:
        new_user = User(username=username, password=password_hash, email=email)
        db.session.add(new_user)
        try:
            db.session.commit()
            print(f"User {username} added successfully.")
        except IntegrityError:
            db.session.rollback()
            print(f"Failed to add user {username}: Duplicate username.")
    else:
        print(f"User {username} already exists.")
=======
    db.session.commit()
    print("Default interests added.")
>>>>>>> e6010eba14b91dd79d2b3c1ba5cd011cb8055512
