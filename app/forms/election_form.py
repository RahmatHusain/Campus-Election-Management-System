from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    IntegerField,
    SelectField,
    SubmitField
)
from wtforms.validators import (
    DataRequired,
    Length,
    NumberRange,
    ValidationError
)

from app.models.position import Position


class PositionForm(FlaskForm):
    """
    Production Position Form

    Used for:
        • Create Position
        • Edit Position
    """

    election_id = SelectField(
        "Election",
        coerce=int,
        validators=[
            DataRequired(message="Please select an election.")
        ]
    )

    title = StringField(
        "Position Title",
        validators=[
            DataRequired(message="Position title is required."),
            Length(
                min=3,
                max=100,
                message="Position title must be between 3 and 100 characters."
            )
        ],
        render_kw={
            "placeholder": "President"
        }
    )

    description = TextAreaField(
        "Description",
        validators=[
            Length(max=500)
        ],
        render_kw={
            "rows": 4,
            "placeholder": "Optional description..."
        }
    )

    max_candidates = IntegerField(
        "Maximum Candidates",
        default=10,
        validators=[
            DataRequired(),
            NumberRange(
                min=1,
                max=100,
                message="Maximum candidates must be between 1 and 100."
            )
        ]
    )

    max_votes = IntegerField(
        "Maximum Votes Per Student",
        default=1,
        validators=[
            DataRequired(),
            NumberRange(
                min=1,
                max=20,
                message="Maximum votes must be between 1 and 20."
            )
        ]
    )

    display_order = IntegerField(
        "Display Order",
        default=1,
        validators=[
            DataRequired(),
            NumberRange(
                min=1,
                max=1000
            )
        ]
    )

    status = SelectField(
        "Status",
        choices=[
            ("active", "Active"),
            ("inactive", "Inactive"),
            ("archived", "Archived")
        ],
        default="active"
    )

    submit = SubmitField("Save Position")

    # --------------------------------------------------
    # Validation
    # --------------------------------------------------

    def validate_title(self, field):
        """
        Prevent duplicate position names
        within the same election.
        """

        if not self.election_id.data:
            return

        existing = Position.query.filter(
            Position.election_id == self.election_id.data,
            Position.title.ilike(field.data.strip())
        ).first()

        if existing:
            raise ValidationError(
                "This position already exists for the selected election."
            )

    def validate_max_votes(self, field):
        """
        Votes cannot exceed
        candidate limit.
        """

        if (
            self.max_candidates.data
            and field.data > self.max_candidates.data
        ):
            raise ValidationError(
                "Maximum votes cannot exceed maximum candidates."
            )