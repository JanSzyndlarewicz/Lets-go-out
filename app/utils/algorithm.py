from typing import Type

from sqlalchemy import ColumnElement, and_
from sqlalchemy.orm import Session

from app.models import BlockingAssociation, MatchingPreferences, Profile, User


def between(column: int, start: any, end: any) -> ColumnElement[bool]:
    return and_(column >= start, column <= end)


def suggest_matches(current_user_id: int, session: Session) -> list[Type[User]]:
    current_user = session.query(User).filter(User.id == current_user_id).first()
    preferences = current_user.matching_preferences

    min_year_of_birth = current_user.profile.year_of_birth - preferences.lower_difference
    max_year_of_birth = current_user.profile.year_of_birth + preferences.upper_difference

    potential_matches = (
        session.query(User)
        .join(Profile)
        .join(MatchingPreferences)
        .filter(
            and_(
                Profile.gender.in_(preferences.gender_preferences),
                between(Profile.year_of_birth, min_year_of_birth, max_year_of_birth),
                User.id != current_user_id,
                ~User.blocking.any(BlockingAssociation.blocked_id == current_user_id),
                ~User.blockers.any(BlockingAssociation.blocker_id == current_user_id),
            )
        )
        .all()
    )
    return potential_matches
