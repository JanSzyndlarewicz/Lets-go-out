from sqlalchemy.orm import Session

from app.models import BlockingAssociation, MatchingPreferences, Profile, User, profile_interests


def between(column, start, end):
    return and_(column >= start, column <= end)


from sqlalchemy import and_, func


def suggest_matches(current_user_id: int, session: Session):
    current_user = session.query(User).filter(User.id == current_user_id).first()
    profile = current_user.profile
    preferences = current_user.matching_preferences

    min_year_of_birth = current_user.profile.year_of_birth - preferences.min_age
    max_year_of_birth = current_user.profile.year_of_birth + preferences.max_age

    potential_matches = (
        session.query(User)
        .join(Profile)
        .join(MatchingPreferences)
        .filter(
            and_(
                Profile.gender == preferences.gender_preference,
                between(Profile.year_of_birth, min_year_of_birth, max_year_of_birth),
                User.id != current_user_id,
                ~User.blocking.any(BlockingAssociation.blocked_id == current_user_id),
                ~User.blockers.any(BlockingAssociation.blocker_id == current_user_id),
            )
        )
        .all()
    )

    potential_matches_with_interests = []
    for match in potential_matches:
        common_interests_count = (
            session.query(func.count(profile_interests.c.interest_id))
            .filter(
                profile_interests.c.profile_id == profile.id,
                profile_interests.c.interest_id.in_(
                    session.query(profile_interests.c.interest_id).filter(
                        profile_interests.c.profile_id == match.profile.id
                    )
                ),
            )
            .scalar()
        )
        potential_matches_with_interests.append((match, common_interests_count))

    potential_matches_with_interests.sort(key=lambda x: x[1], reverse=True)

    for match, _ in potential_matches_with_interests:
        yield match
