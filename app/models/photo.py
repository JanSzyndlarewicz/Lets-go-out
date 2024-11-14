from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.database import db


class Photo(db.Model):
    __tablename__ = "photo"
    id: Mapped[int] = mapped_column(primary_key=True)
    profile: Mapped["Profile"] = relationship("Profile", uselist=False, back_populates="photo")
    file_extension: Mapped[str] = mapped_column(String(8))
