from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash

from app import create_app
from app.models import Gender, Interests, MatchingPreferences, Photo, Profile, User, db

app = create_app()

with app.app_context():
    db.create_all()

    # Adding default interests
    default_interests = [
        "Cooking",
        "Sports",
        "Music",
        "Travel",
        "Reading",
        "Gaming",
    ]
    for interest_name in default_interests:
        if not Interests.query.filter_by(name=interest_name).first():
            new_interest = Interests(name=interest_name)
            db.session.add(new_interest)

    username = "admin"
    password = "admin"  # Hash this in production
    email = "admin"

    name = "Admin"
    gender = Gender.MALE
    year_of_birth = 1999
    description = "this is admin"
    interests = []

    password_hash = generate_password_hash(password)

    existing_user = User.query.filter_by(username=username).first()
    if existing_user is None:

        new_photo = Photo(file_extension="jpg")
        new_profile = Profile(
            name=name,
            gender=gender,
            year_of_birth=year_of_birth,
            description=description,
            interests=interests,
        )
        new_profile.photo = new_photo
        new_user = User(username=username, password=password_hash, email=email)
        new_user.profile = new_profile
        new_preferences = MatchingPreferences(
            user=new_user,
            gender_preferences=[Gender.MALE, Gender.FEMALE],
            lower_difference=10,
            upper_difference=8,
        )

        db.session.add(new_profile)
        db.session.add(new_user)

        try:
            db.session.commit()
            print(f"User {username} added successfully.")
        except IntegrityError as e:
            db.session.rollback()
            print(e)
    else:
        print(f"User {username} already exists.")

    # Adding 15 new users
    new_users = [
        {
            "email": f"user{i}@example.com",
            "username": f"user{i}",
            "password": "password",
            "profile": {
                "name": f"User {i}",
                "gender": Gender.MALE if i % 2 == 0 else Gender.FEMALE,
                "year_of_birth": 1990 + i,
                "description": f"This is user {i}'s profile description.",
            },
            "preferences": {
                "gender_preference": (Gender.FEMALE if i % 2 == 0 else Gender.MALE),
                "min_age": 5,
                "max_age": 5,
            },
        }
        for i in range(1, 16)
    ]

    for user_data in new_users:
        user = User(
            email=user_data["email"],
            username=user_data["username"],
            password=user_data["password"],
        )
        profile = Profile(
            name=user_data["profile"]["name"],
            gender=user_data["profile"]["gender"],
            year_of_birth=user_data["profile"]["year_of_birth"],
            description=user_data["profile"]["description"],
            user=user,
        )
        preferences = MatchingPreferences(
            gender_preferences=[user_data["preferences"]["gender_preference"]],
            lower_difference=user_data["preferences"]["min_age"],
            upper_difference=user_data["preferences"]["max_age"],
            user=user,
        )
        db.session.add(user)
        db.session.add(profile)
        db.session.add(preferences)

    db.session.commit()
    print("Default interests added.")
