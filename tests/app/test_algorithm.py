import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.algorithm import suggest_matches
from app.models import MatchingPreferences, Profile, User, db


@pytest.fixture(scope="function")
def test_session():
    engine = create_engine("sqlite:///:memory:")
    db.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    db.metadata.drop_all(engine)


def create_test_data(session):
    user1 = User(username="user1", email="user1@example.com", password="password")
    profile1 = Profile(
        user_id=1,
        name="User 1",
        gender="male",
        year_of_birth=1991,
        description="User 1's profile",
    )
    preferences1 = MatchingPreferences(
        user_id=1, gender_preferences=["female"], lower_difference=20, upper_difference=30
    )
    user1.profile = profile1
    user1.matching_preferences = preferences1

    user2 = User(username="user2", email="user2@example.com", password="password")
    profile2 = Profile(
        user_id=2,
        name="User 2",
        gender="female",
        year_of_birth=1990,
        description="User 2's profile",
    )
    preferences2 = MatchingPreferences(user_id=2, gender_preferences=["male"], lower_difference=5, upper_difference=5)
    user2.profile = profile2
    user2.matching_preferences = preferences2

    session.add_all([user1, user2])
    session.commit()


def test_suggest_matches(test_session):
    create_test_data(test_session)

    matches = list(suggest_matches(1, test_session))
    print(matches)
    assert len(matches) == 1
    assert matches[0].username == "user2"

    matches = list(suggest_matches(2, test_session))
    print(matches)
    assert len(matches) == 1
    assert matches[0].username == "user1"


def test_no_matches_by_gender(test_session):
    create_test_data(test_session)

    user3 = User(username="user3", email="user3@example.com", password="password")
    profile3 = Profile(
        user_id=3,
        name="User 3",
        gender="female",
        year_of_birth=2000,
        description="User 3's profile",
    )
    preferences3 = MatchingPreferences(
        user_id=3, gender_preferences=["non_binary"], lower_difference=5, upper_difference=5
    )
    user3.profile = profile3
    user3.matching_preferences = preferences3

    test_session.add(user3)
    test_session.commit()

    # Test for user3
    matches = list(suggest_matches(3, test_session))
    assert len(matches) == 0


def test_no_matches_by_age(test_session):
    create_test_data(test_session)

    user3 = User(username="user4", email="user4@example.com", password="password")
    profile3 = Profile(
        user_id=4,
        name="User 4",
        gender="female",
        year_of_birth=2010,
        description="User 4's profile",
    )
    preferences3 = MatchingPreferences(user_id=4, gender_preferences=["female"], lower_difference=1, upper_difference=1)
    user3.profile = profile3
    user3.matching_preferences = preferences3

    test_session.add(user3)
    test_session.commit()

    # Test for user3
    matches = list(suggest_matches(3, test_session))
    assert len(matches) == 0


def test_blocked_users(test_session):
    # Create users, profiles, and matching preferences
    user1 = User(username="user1", email="user1@example.com", password="password")
    profile1 = Profile(
        user_id=1,
        name="User 1",
        gender="female",
        year_of_birth=1991,
        description="User 1's profile",
    )
    preferences1 = MatchingPreferences(user_id=1, gender_preferences=["male"], lower_difference=5, upper_difference=5)
    user1.profile = profile1
    user1.matching_preferences = preferences1

    user2 = User(username="user2", email="user2@example.com", password="password")
    profile2 = Profile(
        user_id=2,
        name="User 2",
        gender="male",
        year_of_birth=1990,
        description="User 2's profile",
    )
    preferences2 = MatchingPreferences(user_id=2, gender_preferences=["female"], lower_difference=5, upper_difference=5)
    user2.profile = profile2
    user2.matching_preferences = preferences2

    user1.blocking.append(user2)

    test_session.add_all([user1, user2])
    test_session.commit()

    matches = list(suggest_matches(1, test_session))
    assert len(matches) == 0

    matches = list(suggest_matches(2, test_session))
    assert len(matches) == 0
