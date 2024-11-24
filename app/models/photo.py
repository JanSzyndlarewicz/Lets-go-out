from app.models.database import db
from flask import current_app, url_for
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Photo(db.Model):
    __tablename__ = "photo"
    id: Mapped[int] = mapped_column(primary_key=True)
    profile: Mapped["Profile"] = relationship(
        "Profile", uselist=False, back_populates="photo"
    )
    file_extension: Mapped[str] = mapped_column(String(8))

    @property
    def flask_photo_url(self) -> str:
        return url_for("static", filename=f"images/{self.id}.{self.file_extension}")

    @property
    def os_photo_url(self) -> str:
        return f"{current_app.config['UPLOAD_FOLDER']}/{self.id}.{self.file_extension}"
