from flask_wtf import FlaskForm
from wtforms import (
    SelectField,
    StringField,
    TextAreaField,
    SubmitField
)
from wtforms.validators import (
    DataRequired,
    Optional,
    Length
)


class CandidateForm(FlaskForm):

    student_id = SelectField(
        "Student",
        choices=[],
        coerce=int,
        validators=[
            DataRequired()
        ]
    )

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
        default="pending",
        validators=[
            DataRequired()
        ]
    )

    submit = SubmitField("Save Candidate")


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