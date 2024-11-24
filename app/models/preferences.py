from app.models.database import db
from app.models.gender import Gender
from sqlalchemy import Enum, ForeignKey, Integer
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import Mapped, mapped_column, relationship


class UserGenderPreference(db.Model):
    __tablename__ = "user_gender_preferences"
    matching_preferences_id: Mapped[int] = mapped_column(
        ForeignKey("matching_preferences.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
    )
    matching_preferences: Mapped["MatchingPreferences"] = relationship(
        "MatchingPreferences", back_populates="genders"
    )
    gender: Mapped["Gender"] = mapped_column(Enum(Gender), primary_key=True)


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
