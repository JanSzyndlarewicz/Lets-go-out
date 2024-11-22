from sqlalchemy import ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship


from app.models.associations import ProfileInterestAssociation
from app.models.database import db


class Interest(db.Model):
    __tablename__ = "interest"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    profiles: Mapped[list["Profile"]] = relationship(
        "Profile",
        secondary=ProfileInterestAssociation.__table__,  
        primaryjoin="Interest.id == ProfileInterestAssociation.interest_id",
        secondaryjoin="Profile.id == ProfileInterestAssociation.profile_id",
        back_populates="interests",
    )

    def __repr__(self):
        return f"<Interest(name={self.name})>"
