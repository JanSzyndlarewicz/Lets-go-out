from sqlalchemy import ForeignKey, Table

from app.models.database import db


class Interests(db.Model):
    __tablename__ = "interests"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f"<Interest(name={self.name})>"


profile_interests = Table(
    "profile_interests",
    db.metadata,
    db.Column("profile_id", db.Integer, ForeignKey("profile.id"), primary_key=True),
    db.Column("interest_id", db.Integer, ForeignKey("interests.id"), primary_key=True),
)
