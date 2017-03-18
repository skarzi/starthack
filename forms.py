from flask_wtf import FlaskForm

from wtforms import (
    BooleanField,
    StringField,
    SubmitField,
    TextAreaField,
    DateField,
)
from wtforms.validators import (
    DataRequired,
    Length,
)

class FlightForm(FlaskForm):
    from_ = StringField('from', validators=[DataRequired()])
    to_ = StringField('to', validators=[DataRequired()])
    departure_ = StringField('departure', validators=[DataRequired()])
    return_ = StringField('return', validators=[DataRequired()])
