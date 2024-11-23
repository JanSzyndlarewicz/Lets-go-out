from datetime import date

from wtforms.validators import ValidationError

def is_not_past(form, field):
    print("validuje date")
    if field.data < date.today():
        raise ValidationError('You cannot choose a date in the past.')