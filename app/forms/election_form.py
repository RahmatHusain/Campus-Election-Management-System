from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    SelectField,
    DateTimeLocalField,
    SubmitField,
)
from wtforms.validators import DataRequired, Length


class ElectionForm(FlaskForm):
    title = StringField(
        "Election Title",
        validators=[DataRequired(), Length(max=150)]
    )

    academic_year = StringField(
        "Academic Year",
        validators=[DataRequired()]
    )

    election_type = SelectField(
        "Election Type",
        choices=[
            ("general", "General"),
            ("department", "Department"),
            ("club", "Club"),
        ],
        validators=[DataRequired()]
    )

    description = TextAreaField("Description")

    start_date = DateTimeLocalField(
        "Start Date",
        format="%Y-%m-%dT%H:%M",
        validators=[DataRequired()]
    )

    end_date = DateTimeLocalField(
        "End Date",
        format="%Y-%m-%dT%H:%M",
        validators=[DataRequired()]
    )

    status = SelectField(
        "Status",
        choices=[
            ("draft", "Draft"),
            ("scheduled", "Scheduled"),
            ("active", "Active"),
            ("completed", "Completed"),
        ]
    )

    submit = SubmitField("Create Election")