from datetime import date

from wtforms.validators import ValidationError

from app.models.tables_config import TablesConfig


def is_not_past(form, field):
    if field.data < date.today():
        raise ValidationError("You cannot choose a date in the past.")

def is_any_table_available_for_date(form, field):
    print(type(field.data))
    print(not TablesConfig.get_is_any_available(field.data))
    print(TablesConfig.get_avaliable_tables_for_day(field.data))
    print(TablesConfig.get_max_tables())
    if not TablesConfig.get_is_any_available(field.data):
        raise ValidationError("No tables available for chosen date")