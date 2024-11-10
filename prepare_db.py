from app import create_app

from sqlalchemy.exc import IntegrityError

from werkzeug.security import generate_password_hash

from app.models import db, User, Interests, Profile, Gender, Photo

app = create_app()

with app.app_context():
    db.create_all()

    # Adding default interests
    default_interests = ['Cooking', 'Sports', 'Music', 'Travel', 'Reading', 'Gaming']
    for interest_name in default_interests:
        if not Interests.query.filter_by(name=interest_name).first():
            new_interest = Interests(name=interest_name)
            db.session.add(new_interest)

    username = 'admin'
    password = 'admin'  # Hash this in production
    email = 'admin'

    name = "Admin"
    gender = Gender.other
    year_of_birth = 1999
    description = "this is admin"
    interests = []

    password_hash = generate_password_hash(password)

    existing_user = User.query.filter_by(username=username).first()
    if existing_user is None:
        new_photo = Photo(file_extension="jpg")
        new_profile = Profile(name=name, gender=gender, year_of_birth=year_of_birth, description=description, interests=interests)
        new_profile.photo = new_photo
        new_user = User(username=username, password=password_hash, email=email)
        new_user.profile = new_profile
        db.session.add(new_profile)
        db.session.add(new_user)  
        try:
            db.session.commit()
            print(f"User {username} added successfully.")
        except IntegrityError as e:
            db.session.rollback()
            print(e)
            #print(f"Failed to add user {username}: Duplicate username.")
    else:
        print(f"User {username} already exists.")
    db.session.commit()
    print("Default interests added.")

