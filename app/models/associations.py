from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.models.database import db


class LikingAssociation(db.Model):
    __tablename__ = "liking_association"
    liker_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    liked_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)


class BlockingAssociation(db.Model):
    __tablename__ = "blocking_association"
    blocker_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    blocked_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)


class RejectedAssociation(db.Model):
    """model that stores data useful for filtering users for date invitation.
    Note it has a created_date field, which can be the indicator for wether the
    rejected should reappear for rejecting reconsideration (should row be deleted after a certain time?)"""

    __tablename__ = "rejected_association"
    rejecter_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    rejected_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    created_date: Mapped[datetime] = mapped_column(db.DateTime, default=datetime.now)


class ProfileInterestAssociation(db.Model):
    __tablename__ = "profile_interest_association"
    profile_id = db.Column(db.Integer, db.ForeignKey("profile.id"), primary_key=True)
    interest_id = db.Column(db.Integer, db.ForeignKey("interest.id"), primary_key=True)
