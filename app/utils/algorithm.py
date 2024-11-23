from typing import Type

from flask_login import current_user
from sqlalchemy import ColumnElement, and_
from sqlalchemy.orm import Session

from app.models import BlockingAssociation, MatchingPreferences, Profile, ProfileInterestAssociation, User


def between(column: int, start: any, end: any) -> ColumnElement[bool]:
    return and_(column >= start, column <= end)


def suggest_matches(session: Session, user_id: int = None, number: int = None) -> list[Type[User]]:
    if user_id is None:
        user_id = current_user.id
    user = session.query(User).filter(User.id == user_id).first()
    preferences = user.matching_preferences

    min_year_of_birth = user.profile.year_of_birth - preferences.lower_difference
    max_year_of_birth = user.profile.year_of_birth + preferences.upper_difference

    potential_matches = (
        session.query(User)
        .join(Profile)
        .join(MatchingPreferences)
        .filter(
            and_(
                Profile.gender.in_(preferences.gender_preferences),
                between(Profile.year_of_birth, min_year_of_birth, max_year_of_birth),
                User.id != user_id,
                ~User.blocking.any(BlockingAssociation.blocked_id == user_id),
                ~User.blockers.any(BlockingAssociation.blocker_id == user_id),
                ~User.rejected.any(BlockingAssociation.blocked_id == user_id),
                ~User.rejecters.any(BlockingAssociation.blocker_id == user_id),
                Profile.interests.any(
                    ProfileInterestAssociation.interest_id.in_([interest.id for interest in user.profile.interests])
                ),
            )
        )
    )
    if number:
        potential_matches = potential_matches.limit(number).all()
    else:
        potential_matches = potential_matches.all()
    return potential_matches
