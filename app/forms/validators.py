from datetime import date, datetime

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
    
def age_limit(form, field):
    yob = field.data
    age = datetime.now().year - yob
    if age < 0:
        raise ValidationError("You cannot use this service if you haven't been born yet!")
    if age < 18:
        raise ValidationError("Apologies, you cannot use this service if you are underage.")
    if age > 120:
        raise ValidationError("Year of birth cannot be more than 120 years in the past.")