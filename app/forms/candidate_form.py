from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import Optional, Length, DataRequired


class CandidateEditForm(FlaskForm):

    slogan = StringField(
        "Slogan",
        validators=[
            Optional(),
            Length(max=255)
        ]
    )

    manifesto = TextAreaField(
        "Manifesto",
        validators=[
            Optional()
        ]
    )

    symbol = StringField(
        "Election Symbol",
        validators=[
            Optional(),
            Length(max=255)
        ]
    )

    status = SelectField(
        "Status",
        choices=[
            ("pending", "Pending"),
            ("approved", "Approved"),
            ("rejected", "Rejected"),
            ("withdrawn", "Withdrawn")
        ],
        validators=[
            DataRequired()
        ]
    )

    submit = SubmitField("Save Changes")