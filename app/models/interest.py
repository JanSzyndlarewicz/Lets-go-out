from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.associations import ProfileInterestAssociation
from app.models.database import db


class Interest(db.Model):
    __tablename__ = "interest"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    profiles: Mapped[list["Profile"]] = relationship(
        "Profile",
        secondary=ProfileInterestAssociation.__table__,
        primaryjoin="Interest.id == ProfileInterestAssociation.interest_id",
        secondaryjoin="Profile.id == ProfileInterestAssociation.profile_id",
        back_populates="interests",
    )

    def __repr__(self):
        return f"<Interest(name={self.name})>"
