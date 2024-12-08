import datetime
import random

from faker import Faker

from sqlalchemy.exc import IntegrityError

from app import create_app
from app.models import Gender, Interest, MatchingPreferences, Photo, Profile, User
from app.models.associations import ProfileInterestAssociation
from app.models.database import db
from app.models.date_proposal import DateProposal
from app.utils import constants

def add_invites():
    users = User.query.all()
    for user in users:
        for _ in range(3):
            invitee = random.choice(users)
            if invitee != user:
                db.session.add(DateProposal(
                    proposer = user,
                    recipient = invitee,
                    date = datetime.datetime.today() + datetime.timedelta(days=random.randint(1,7))
                ))
    db.session.commit()

def add_likes():
    users = User.query.all()
    for user in users:
        liked = random.choice(users)
        if liked != user:
            user.liking.append(liked)
    db.session.commit()

def add_blocks():
    users = User.query.all()
    for user in users:
        if random.random() > 0.5:
            blocked = random.choice(users)
            if blocked != user:
                user.blocking.append(blocked)
    db.session.commit()


app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    # Adding default interests
    default_interests = constants.interests
    for interest_name in default_interests:
        if not Interest.query.filter_by(name=interest_name).first():
            new_interest = Interest(name=interest_name)
            db.session.add(new_interest)

    # Adding admin user
    username = "admin"
    password = "admin"
    email = "admin"
    name = "Admin"
    gender = Gender.MALE
    year_of_birth = 1999
    description = "this is admin"
    interests = Interest.query.limit(2).all()

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
        new_user = User(username=username, password=password, email=email, confirmed=True)
        new_user.profile = new_profile
        new_preferences = MatchingPreferences(
            user=new_user,
            gender_preferences=[Gender.MALE, Gender.FEMALE],
            lower_difference=8,
            upper_difference=4,
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

    f = Faker()
    # Adding 15 new users
    new_users = [
        {
            "email": f"user{i}@example.com",
            "username": f"user{i}",
            "password": "password",
            "profile": {
                "name": f.first_name_male() if i % 2 == 0 else f.first_name_female(),
                "gender": Gender.MALE if i % 2 == 0 else Gender.FEMALE,
                "year_of_birth": random.randint(1980, 2003),
                "description": f"This is user {i}'s profile description.",
            },
            "preferences": {
                "gender_preference": (Gender.FEMALE if i % 2 == 0 else Gender.MALE),
                "min_age": 5,
                "max_age": 5,
            },
        }
        for i in range(1, 100)
    ]

    for user_data in new_users:
        user = User(
            email=user_data["email"],
            username=user_data["username"],
            password=user_data["password"],
            confirmed=True
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

        # Add user, profile, preferences, then commit to generate profile ID
        db.session.add(user)
        db.session.add(profile)
        db.session.add(preferences)
        db.session.commit()  # Commit here to generate profile.id

        # Now that the profile.id is available, create the associations
        interests = Interest.query.all()

        if not Profile.query.filter_by(id=profile.id).first().interests:
            profile_interests = [
                ProfileInterestAssociation(
                    profile_id=profile.id,
                    interest_id=interests[i].id,
                )
                for i in random.sample(range(len(interests)), k=random.randint(0, 6))
            ]

            db.session.add_all(profile_interests)
        db.session.commit()  # Commit associations

    add_invites()
    add_likes()
    add_blocks()

    print("DB prepared.")


