
from datetime import datetime

from sqlalchemy import func, or_

from app.models.date_proposal import DateProposal, ProposalStatus
from app.models.database import db


class TablesConfig :
    __MAX_TABLES_FOR_DAY = 2
    
    @staticmethod
    def get_avaliable_tables_for_day(date: datetime) -> int:
        proposals_for_day_count = (
            db.session
            .query(DateProposal)
            .filter(
                func.date(DateProposal.date) == date,
                DateProposal.status.in_([ProposalStatus.accepted.name, ProposalStatus.proposed.name])
            )
            .count()
        )
        return TablesConfig.__MAX_TABLES_FOR_DAY - proposals_for_day_count
    
    @staticmethod
    def get_is_any_available(date: datetime) -> bool:
        return TablesConfig.get_avaliable_tables_for_day(date) > 0
    
    @staticmethod
    def get_max_tables():
        return TablesConfig.__MAX_TABLES_FOR_DAY