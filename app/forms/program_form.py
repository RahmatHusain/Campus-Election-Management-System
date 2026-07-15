from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    IntegerField,
    TextAreaField,
    BooleanField,
    SelectField,
    SubmitField
)
from wtforms.validators import (
    DataRequired,
    Length,
    NumberRange,
    ValidationError
)

from app.models.department import Department
from app.models.program import Program


class ProgramForm(FlaskForm):

    department_id = SelectField(
        "Department",
        coerce=int,
        validators=[DataRequired()]
    )

    name = StringField(
        "Program Name",
        validators=[
            DataRequired(),
            Length(min=2, max=100)
        ]
    )

    code = StringField(
        "Program Code",
        validators=[
            DataRequired(),
            Length(min=2, max=20)
        ]
    )

    duration_years = IntegerField(
        "Duration (Years)",
        validators=[
            DataRequired(),
            NumberRange(min=1, max=8)
        ],
        default=4
    )

    total_semesters = IntegerField(
        "Total Semesters",
        validators=[
            DataRequired(),
            NumberRange(min=1, max=16)
        ],
        default=8
    )

    description = TextAreaField(
        "Description"
    )

    is_active = BooleanField(
        "Active",
        default=True
    )

    submit = SubmitField(
        "Save Program"
    )

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.department_id.choices = [

            (d.id, f"{d.name} ({d.faculty.name})")

            for d in Department.query.order_by(
                Department.name
            ).all()

        ]

    def validate_name(self, field):

        existing = Program.query.filter_by(
            department_id=self.department_id.data,
            name=field.data.strip()
        ).first()

        if existing:

            raise ValidationError(
                "Program already exists in this department."
            )

    def validate_code(self, field):

        existing = Program.query.filter_by(
            department_id=self.department_id.data,
            code=field.data.strip()
        ).first()

        if existing:

            raise ValidationError(
                "Program Code already exists."
            )