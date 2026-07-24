from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    SelectField,
    DateTimeLocalField,
    SubmitField,
)
from wtforms.validators import (
    DataRequired,
    Length,
    ValidationError,
)


class ElectionForm(FlaskForm):

    title = StringField(
        "Election Title",
        validators=[
            DataRequired(),
            Length(max=200)
        ]
    )

    academic_year = StringField(
        "Academic Year",
        validators=[
            DataRequired(),
            Length(max=20)
        ]
    )

    election_type = SelectField(
        "Election Type",
        choices=[
            ("general", "General Election"),
            ("department", "Department Election"),
            ("club", "Club Election"),
        ],
        validators=[DataRequired()]
    )

    description = TextAreaField(
        "Description"
    )

    start_datetime = DateTimeLocalField(
        "Start Date & Time",
        format="%Y-%m-%dT%H:%M",
        validators=[DataRequired()]
    )

    end_datetime = DateTimeLocalField(
        "End Date & Time",
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
        ],
        default="draft"
    )

    submit = SubmitField("Create Election")

    def validate_end_datetime(self, field):
        if (
            self.start_datetime.data
            and field.data
            and field.data <= self.start_datetime.data
        ):
            raise ValidationError(
                "End Date must be after Start Date."
            )