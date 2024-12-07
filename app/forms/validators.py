from datetime import date

from wtforms.validators import ValidationError

from app.models.tables_config import TablesConfig

from app import db, User


def is_not_past(form, field):
    if field.data < date.today():
        raise ValidationError("You cannot choose a date in the past.")

def is_any_table_available_for_date(form, field):
    if not TablesConfig.get_is_any_available(field.data):
        raise ValidationError("No tables available for chosen date")
    
def username_unique(form, field):
    user = User.query.filter_by(username=field.data).first()
    if user is not None:
        raise ValidationError("This username is already taken.")
    
def email_unique(form, field):
    user = User.query.filter_by(email=field.data).first()
    if user is not None:
        raise ValidationError("This email address is already taken.")