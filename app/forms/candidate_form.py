from flask_wtf import FlaskForm
from wtforms import (
    SelectField,
    TextAreaField,
    SubmitField
)
from wtforms.validators import DataRequired, Length


class CandidateForm(FlaskForm):
    """
    Candidate Create/Edit Form
    """

    student_id = SelectField(
        "Student",
        coerce=int,
        validators=[
            DataRequired()
        ]
    )

    position_id = SelectField(
        "Position",
        coerce=int,
        validators=[
            DataRequired()
        ]
    )

    manifesto = TextAreaField(
        "Manifesto",
        validators=[
            Length(max=2000)
        ],
        render_kw={
            "rows": 6,
            "placeholder": "Candidate manifesto..."
        }
    )

    submit = SubmitField("Save Candidate")