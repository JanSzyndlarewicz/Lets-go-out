# app/models.py
import enum
from datetime import datetime
from typing import Optional

from flask import current_app as app
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from itsdangerous import URLSafeTimedSerializer
from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Integer, String, Table
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()
Base = declarative_base()


class Gender(enum.Enum):
    MALE = "Male"
    FEMALE = "Female"
    NON_BINARY = "Non binary"
    OTHER = "Other"


class Interests(db.Model):
    __tablename__ = "interests"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f"<Interest(name={self.name})>"


profile_interests_table = Table(
    "profile_interests",
    db.metadata,
    db.Column("profile_id", db.Integer, ForeignKey("profile.id"), primary_key=True),
    db.Column("interest_id", db.Integer, ForeignKey("interests.id"), primary_key=True),
)


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(128), nullable=False)
    confirmed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    profile: Mapped["Profile"] = relationship("Profile", uselist=False, back_populates="user")
    matching_preferences: Mapped["MatchingPreferences"] = relationship(
        "MatchingPreferences", uselist=False, back_populates="user"
    )
    liking: Mapped[list["User"]] = relationship(
        "User",
        secondary="liking_association",
        primaryjoin="User.id == LikingAssociation.liker_id",
        secondaryjoin="User.id == LikingAssociation.liked_id",
        back_populates="likers",
    )
    likers: Mapped[list["User"]] = relationship(
        "User",
        secondary="liking_association",
        primaryjoin="User.id == LikingAssociation.liked_id",
        secondaryjoin="User.id == LikingAssociation.liker_id",
        back_populates="liking",
    )
    blocking: Mapped[list["User"]] = relationship(
        "User",
        secondary="blocking_association",
        primaryjoin="User.id == BlockingAssociation.blocker_id",
        secondaryjoin="User.id == BlockingAssociation.blocked_id",
        back_populates="blockers",
    )
    blockers: Mapped[list["User"]] = relationship(
        "User",
        secondary="blocking_association",
        primaryjoin="User.id == BlockingAssociation.blocked_id",
        secondaryjoin="User.id == BlockingAssociation.blocker_id",
        back_populates="blocking",
    )
    sent_proposals: Mapped[list["DateProposal"]] = relationship(
        "DateProposal",
        back_populates="proposer",
        foreign_keys="DateProposal.proposer_id",
    )
    received_proposals: Mapped[list["DateProposal"]] = relationship(
        "DateProposal",
        back_populates="recipient",
        foreign_keys="DateProposal.recipient_id",
    )

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def has_preference_for(self, gender_value: str) -> bool:
        return Gender[gender_value] in self.matching_preferences.gender_preferences

    def generate_token(self):
        serializer = URLSafeTimedSerializer(app.secret_key)
        return serializer.dumps(self.id, salt="confirmation_token")

    def confirm(self, token):
        serializer = URLSafeTimedSerializer(app.secret_key)
        try:
            serializer.loads(token, salt="confirmation_token", max_age=3600)
            self.confirmed = True
            return True
        except:
            return False


class Profile(db.Model):
    __tablename__ = "profile"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), unique=True)
    user: Mapped["User"] = relationship("User", back_populates="profile")
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    gender: Mapped[Gender] = mapped_column(Enum(Gender), nullable=False)
    year_of_birth: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=True)
    photo_id: Mapped[Optional[int]] = mapped_column(ForeignKey("photo.id"))
    photo: Mapped[Optional["Photo"]] = relationship("Photo", back_populates="profile")
    interests = relationship("Interests", secondary=profile_interests_table, backref="profiles")


class Photo(db.Model):
    __tablename__ = "photo"
    id: Mapped[int] = mapped_column(primary_key=True)
    profile: Mapped["Profile"] = relationship("Profile", uselist=False, back_populates="photo")
    file_extension: Mapped[str] = mapped_column(String(8))


class ProposalStatus(enum.Enum):
    proposed = 1
    accepted = 2
    rejected = 3
    ignored = 4
    reschedule = 5


class DateProposal(db.Model):
    __tablename__ = "date_proposal"
    id: Mapped[int] = mapped_column(primary_key=True)
    proposer_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    recipient_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    status: Mapped["ProposalStatus"] = mapped_column(
        Enum(ProposalStatus), nullable=False, default=ProposalStatus.proposed
    )
    proposal_message: Mapped[Optional[str]] = mapped_column(String(250))
    response_message: Mapped[Optional[str]] = mapped_column(String(250))
    proposal_timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    response_timestamp: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    proposer: Mapped["User"] = relationship("User", back_populates="sent_proposals", foreign_keys=[proposer_id])
    recipient: Mapped["User"] = relationship("User", back_populates="received_proposals", foreign_keys=[recipient_id])


class LikingAssociation(db.Model):
    __tablename__ = "liking_association"
    liker_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    liked_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)


class BlockingAssociation(db.Model):
    __tablename__ = "blocking_association"
    blocker_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    blocked_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)


class UserGenderPreference(db.Model):
    __tablename__ = "user_gender_preferences"
    matching_preferences_id: Mapped[int] = mapped_column(
        ForeignKey("matching_preferences.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
    )
    matching_preferences: Mapped["MatchingPreferences"] = relationship("MatchingPreferences", back_populates="genders")
    gender: Mapped[Gender] = mapped_column(Enum(Gender), primary_key=True)


class MatchingPreferences(db.Model):
    __tablename__ = "matching_preferences"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), unique=True)
    user: Mapped["User"] = relationship("User", back_populates="matching_preferences")
    genders = relationship(
        "UserGenderPreference",
        back_populates="matching_preferences",
        cascade="all, delete-orphan",
    )
    gender_preferences = association_proxy(
        "genders",
        "gender",
        creator=lambda gender: UserGenderPreference(gender=gender),
        cascade_scalar_deletes=True,
    )
    lower_difference = mapped_column(Integer, nullable=False)
    upper_difference = mapped_column(Integer, nullable=False)
