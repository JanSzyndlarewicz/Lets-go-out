from app import create_app
from app.models import Interests, MatchingPreferences, Profile, User, db

app = create_app()

with app.app_context():
    db.create_all()

    # Adding default interests
    default_interests = ["Cooking", "Sports", "Music", "Travel", "Reading", "Gaming"]
    for interest_name in default_interests:
        if not Interests.query.filter_by(name=interest_name).first():
            new_interest = Interests(name=interest_name)
            db.session.add(new_interest)

    # Adding 15 new users
    new_users = [
        {
            "email": f"user{i}@example.com",
            "username": f"user{i}",
            "password": "password",
            "profile": {
                "name": f"User {i}",
                "gender": "male" if i % 2 == 0 else "female",
                "year_of_birth": 1990 + i,
                "description": f"This is user {i}'s profile description.",
            },
            "preferences": {
                "gender_preference": "female" if i % 2 == 0 else "male",
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
            gender_preference=user_data["preferences"]["gender_preference"],
            min_age=user_data["preferences"]["min_age"],
            max_age=user_data["preferences"]["max_age"],
            user=user,
        )
        db.session.add(user)
        db.session.add(profile)
        db.session.add(preferences)

    db.session.commit()
