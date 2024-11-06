# app/models.py
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
import enum
from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Mapped, mapped_column

db = SQLAlchemy()
Base = declarative_base()

class Gender(enum.Enum):
    male = "male"
    female = "female"
    non_binary = "non_binary"
    other = "other"

user_gender_preferences = Table(
    'user_gender_preferences',
    Base.metadata,
    Column('matching_preferences_id', ForeignKey('matching_preferences.id'), primary_key=True),
    Column('gender', Enum(Gender), primary_key=True)
)

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)  # Added username attribute
    password: Mapped[str] = mapped_column(String(128), nullable=False)
    profile: Mapped["Profile"] = relationship("Profile", uselist=False, back_populates="user")
    matching_preferences: Mapped["MatchingPreferences"] = relationship("MatchingPreferences", uselist=False, back_populates="user")
    liking: Mapped[list["User"]] = relationship("User", secondary="liking_association", primaryjoin="User.id == LikingAssociation.liker_id", secondaryjoin="User.id == LikingAssociation.liked_id", back_populates="likers")
    likers: Mapped[list["User"]] = relationship("User", secondary="liking_association", primaryjoin="User.id == LikingAssociation.liked_id", secondaryjoin="User.id == LikingAssociation.liker_id", back_populates="liking")
    blocking: Mapped[list["User"]] = relationship("User", secondary="blocking_association", primaryjoin="User.id == BlockingAssociation.blocker_id", secondaryjoin="User.id == BlockingAssociation.blocked_id", back_populates="blockers")
    blockers: Mapped[list["User"]] = relationship("User", secondary="blocking_association", primaryjoin="User.id == BlockingAssociation.blocked_id", secondaryjoin="User.id == BlockingAssociation.blocker_id", back_populates="blocking")
    sent_proposals: Mapped[list["DateProposal"]] = relationship("DateProposal", back_populates="proposer", foreign_keys="DateProposal.proposer_id")
    received_proposals: Mapped[list["DateProposal"]] = relationship("DateProposal", back_populates="recipient", foreign_keys="DateProposal.recipient_id")


class Profile(db.Model):
    __tablename__ = 'profile'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), unique=True)
    user: Mapped["User"] = relationship("User", back_populates="profile")
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    gender: Mapped[str] = mapped_column(String(50), nullable=False)
    year_of_birth: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=True)
    photo_id: Mapped[int] = mapped_column(ForeignKey('photo.id'))
    photo: Mapped[Optional["Photo"]] = relationship("Photo", foreign_keys=[photo_id], uselist=False, backref="profile")

class Photo(db.Model):
    __tablename__ = 'photo'
    id: Mapped[int] = mapped_column(primary_key=True)
    profile_id: Mapped[int] = mapped_column(ForeignKey("profile.id"))
    file_extension: Mapped[str] = mapped_column(String(8))

class ProposalStatus(enum.Enum):
    proposed = 1
    accepted = 2
    rejected = 3
    ignored = 4
    reschedule = 5

class DateProposal(db.Model):
    __tablename__ = 'date_proposal'
    id: Mapped[int] = mapped_column(primary_key=True)
    proposer_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    recipient_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    status: Mapped["ProposalStatus"] = mapped_column(Enum(ProposalStatus), nullable=False, default=ProposalStatus.proposed)
    proposal_message: Mapped[Optional[str]] = mapped_column(String(250))
    response_message: Mapped[Optional[str]] = mapped_column(String(250))
    proposal_timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    response_timestamp: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    proposer: Mapped["User"] = relationship("User", back_populates="sent_proposals", foreign_keys=[proposer_id])
    recipient: Mapped["User"] = relationship("User", back_populates="received_proposals", foreign_keys=[recipient_id])

class LikingAssociation(db.Model):
    __tablename__ = 'liking_association'
    liker_id: Mapped[int] = mapped_column(ForeignKey('user.id'), primary_key=True)
    liked_id: Mapped[int] = mapped_column(ForeignKey('user.id'), primary_key=True)

class BlockingAssociation(db.Model):
    __tablename__ = 'blocking_association'
    blocker_id: Mapped[int] = mapped_column(ForeignKey('user.id'), primary_key=True)
    blocked_id: Mapped[int] = mapped_column(ForeignKey('user.id'), primary_key=True)

class MatchingPreferences(db.Model):
    __tablename__ = 'matching_preferences'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), unique=True)
    user: Mapped["User"] = relationship("User", back_populates="matching_preferences")