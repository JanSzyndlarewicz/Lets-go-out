from app import create_app
from app.models import User, db
from sqlalchemy.exc import IntegrityError

app = create_app()

# Establish application context
with app.app_context():
    # Create all tables
    db.create_all()

    if 'user' in db.metadata.tables:
        print("User model is registered with the db instance.")
    else:
        print("User model is NOT registered with the db instance.")

    username = 'admin'
    password = 'admin'  # Hash this in production

    existing_user = User.query.filter_by(username=username).first()
    if existing_user is None:
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        try:
            db.session.commit()
            print(f"User {username} added successfully.")
        except IntegrityError:
            db.session.rollback()
            print(f"Failed to add user {username}: Duplicate username.")
    else:
        print(f"User {username} already exists.")