from datetime import date
from typing import Optional

from flask import current_app as app, url_for
from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer
from sqlalchemy import Boolean, Enum, ForeignKey, Integer, String, or_
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import check_password_hash, generate_password_hash

from app.models.associations import ProfileInterestAssociation
from app.models.database import db
from app.models.date_proposal import DateProposal
from app.models.gender import Gender
from app.models.interest import Interest
from app.models.preferences import MatchingPreferences


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(128), nullable=False)
    confirmed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    profile: Mapped["Profile"] = relationship(
        "Profile", uselist=False, back_populates="user"
    )
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
    # TODO: test
    rejected: Mapped[list["User"]] = relationship(
        "User",
        secondary="rejected_association",
        primaryjoin="User.id == RejectedAssociation.rejecter_id",
        secondaryjoin="User.id == RejectedAssociation.rejected_id",
        back_populates="rejecters",
    )
    rejecters: Mapped[list["User"]] = relationship(
        "User",
        secondary="rejected_association",
        primaryjoin="User.id == RejectedAssociation.rejected_id",
        secondaryjoin="User.id == RejectedAssociation.rejecter_id",
        back_populates="rejected",
    )

    def __init__(self, email: str, username: str, password: str, **kwargs):
        self.email = email
        self.username = username
        self.set_password(password)
        self.confirmed = kwargs.get("confirmed", False)
        self.profile = Profile(user=self)
        self.matching_preferences = MatchingPreferences(user=self)

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
    interests: Mapped[list[Optional["Interest"]]] = relationship(
        "Interest",
        secondary=ProfileInterestAssociation.__table__,
        back_populates="profiles",
    )

    @property
    def age(self):
        today = date.today()
        return today.year - self.year_of_birth

    @property
    def profile_picture_url_or_default(self):
        if self.photo is not None:
            return self.photo.flask_photo_url
        return url_for("static", filename="images/default-profile-picture.jpg")

    @property
    def proposals_sent_by_self(self):
        return (
            db.session.query(DateProposal)
            .filter(DateProposal.proposer_id == self.user_id)
            .all()
        )

    @property
    def accepted_proposals_by_either(self):
        return (
            db.session.query(DateProposal)
            .filter(
                or_(
                    DateProposal.proposer_id == self.user_id,
                    DateProposal.recipient_id == self.user_id,
                ),
                DateProposal.status == "accepted",
            )
            .all()
        )

    @property
    def proposed_and_ignored_proposals_by_self(self):
        return (
            db.session.query(DateProposal)
            .filter(
                DateProposal.proposer_id == self.user_id,
                DateProposal.status.in_(["ignored", "proposed"]),
            )
            .all()
        )

    @property
    def accepted_proposals_by_self(self):
        return (
            db.session.query(DateProposal)
            .filter(
                DateProposal.proposer_id == self.user_id,
                DateProposal.status == "accepted",
            )
            .all()
        )

    @property
    def rejected_proposals_by_self(self):
        return (
            db.session.query(DateProposal)
            .filter(
                DateProposal.proposer_id == self.user_id,
                DateProposal.status == "rejected",
            )
            .all()
        )

    @property
    def reschedule_proposals_by_self(self):
        return (
            db.session.query(DateProposal)
            .filter(
                DateProposal.proposer_id == self.user_id,
                DateProposal.status == "reschedule",
            )
            .all()
        )
