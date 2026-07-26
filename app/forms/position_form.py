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
    NumberRange
)


class PositionForm(FlaskForm):

    title = StringField(
        "Position Title",
        validators=[
            DataRequired(),
            Length(min=3, max=100)
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
            "placeholder": "Position description..."
        }
    )

    max_candidates = IntegerField(
        "Maximum Candidates",
        default=10,
        validators=[
            DataRequired(),
            NumberRange(
                min=1,
                max=100
            )
        ]
    )

    max_votes = IntegerField(
        "Maximum Votes Allowed",
        default=1,
        validators=[
            DataRequired(),
            NumberRange(
                min=1,
                max=20
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
                max=100
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