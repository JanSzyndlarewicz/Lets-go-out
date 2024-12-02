import random
from typing import Type

from flask_login import current_user
from sqlalchemy import ColumnElement, and_
from sqlalchemy.orm import Session

from app.models import (
    BlockingAssociation,
    DateProposal,
    LikingAssociation,
    MatchingPreferences,
    Profile,
    ProfileInterestAssociation,
    RejectedAssociation,
    User,
    UserGenderPreference,
)


def between(column: int, start: any, end: any) -> ColumnElement[bool]:
    return and_(column >= start, column <= end)


def suggest_matches(
    session: Session,
    user_id: int = None,
    number: int = None,
    ignore_ids: list[int] = [],
) -> list[Type[User]]:
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
                MatchingPreferences.genders.any(UserGenderPreference.gender == user.profile.gender),
                between(Profile.year_of_birth, min_year_of_birth, max_year_of_birth),
                between(
                    user.profile.year_of_birth,
                    Profile.year_of_birth - MatchingPreferences.lower_difference,
                    Profile.year_of_birth + MatchingPreferences.upper_difference,
                ),
                User.id != user_id,
                ~User.blockers.any(BlockingAssociation.blocker_id == user_id),
                ~User.rejecters.any(RejectedAssociation.rejecter_id == user_id),
                ~User.likers.any(LikingAssociation.liker_id == user_id),
                ~User.sent_proposals.any(DateProposal.recipient_id == user_id),
                ~User.received_proposals.any(DateProposal.proposer_id == user_id),
                ~(User.id.in_(ignore_ids)),
            )
        )
    )
    potential_matches = potential_matches.all()
    if number is not None and number < len(potential_matches):
        weights = []
        for potential_match in potential_matches:
            weight = 2 ** len(set(current_user.profile.interests).intersection(potential_match.profile.interests))
            #print(f"user {potential_match.id}: interests: {potential_match.profile.interests}, weight: {weight}")
            weights.append(weight)
        potential_matches = weighted_sample_without_replacement(potential_matches, weights, number)
    
    return potential_matches

def weighted_sample_without_replacement(elems, weights, k):
    if k >= len(elems):
        return elems
    elems = list(elems)
    weights = list(weights)
    indices = range(len(elems))
    picks = []
    while len(picks) < k:
        for i in random.choices(indices, weights=weights, k=k-len(picks)):
            if weights[i]:
                weights[i] = 0
                picks.append(elems[i])
    return picks