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
    """
    Production Election Form

    Used for:
    - Create Election
    - Edit Election
    """

    title = StringField(
        "Election Title",
        validators=[
            DataRequired(message="Election title is required."),
            Length(
                min=3,
                max=200,
                message="Title must be between 3 and 200 characters."
            )
        ],
        render_kw={
            "placeholder": "BIT Student Election 2026"
        }
    )

    academic_year = StringField(
        "Academic Year",
        validators=[
            DataRequired(message="Academic year is required."),
            Length(max=20)
        ],
        render_kw={
            "placeholder": "2025/2026"
        }
    )

    election_type = SelectField(
        "Election Type",
        choices=[
            ("general", "General Election"),
            ("department", "Department Election"),
            ("club", "Club Election")
        ],
        validators=[
            DataRequired(message="Please select election type.")
        ]
    )

    description = TextAreaField(
        "Description",
        validators=[
            Length(max=1000)
        ],
        render_kw={
            "rows": 4,
            "placeholder": "Election description..."
        }
    )

    start_datetime = DateTimeLocalField(
        "Start Date & Time",
        format="%Y-%m-%dT%H:%M",
        validators=[
            DataRequired(message="Start date is required.")
        ]
    )

    end_datetime = DateTimeLocalField(
        "End Date & Time",
        format="%Y-%m-%dT%H:%M",
        validators=[
            DataRequired(message="End date is required.")
        ]
    )

    status = SelectField(
        "Status",
        choices=[
            ("draft", "Draft"),
            ("scheduled", "Scheduled"),
            ("active", "Active"),
            ("completed", "Completed"),
            ("archived", "Archived"),
        ],
        default="draft"
    )

    submit = SubmitField("Save Election")

    def validate_end_datetime(self, field):
        """
        End date must be after start date.
        """
        if (
            self.start_datetime.data
            and field.data
            and field.data <= self.start_datetime.data
        ):
            raise ValidationError(
                "End date must be later than start date."
            )