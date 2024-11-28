import enum
from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.database import db


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
    proposal_timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    response_timestamp: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    proposer: Mapped["User"] = relationship("User", back_populates="sent_proposals", foreign_keys=[proposer_id])
    recipient: Mapped["User"] = relationship("User", back_populates="received_proposals", foreign_keys=[recipient_id])

    def change_status(self, status, message=None):
        self.status = status
        self.response_timestamp = datetime.now()
        if message is not None:
            self.response_message = message
