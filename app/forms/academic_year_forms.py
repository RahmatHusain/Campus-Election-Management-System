from datetime import date

from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    DateField,
    BooleanField,
    SubmitField
)
from wtforms.validators import (
    DataRequired,
    Length,
    ValidationError
)

from app.models.academic_year import AcademicYear


class AcademicYearForm(FlaskForm):

    name = StringField(
        "Academic Year",
        validators=[
            DataRequired(),
            Length(min=4, max=20)
        ]
    )

    start_date = DateField(
        "Start Date",
        validators=[DataRequired()]
    )

    end_date = DateField(
        "End Date",
        validators=[DataRequired()]
    )

    is_current = BooleanField(
        "Set as Current Academic Year"
    )

    is_active = BooleanField(
        "Active",
        default=True
    )

    submit = SubmitField("Save Academic Year")

    # -----------------------------
    # Validation
    # -----------------------------

    def validate_name(self, field):

        existing = AcademicYear.query.filter_by(
            name=field.data.strip()
        ).first()

        if existing:
            raise ValidationError(
                "Academic Year already exists."
            )

    def validate_end_date(self, field):

        if field.data <= self.start_date.data:
            raise ValidationError(
                "End Date must be after Start Date."
            )

    def validate_start_date(self, field):

        if field.data.year < 2000:
            raise ValidationError(
                "Invalid academic year."
            )

        if field.data < date(2000, 1, 1):
            raise ValidationError(
                "Start Date is not valid."
            )
class EditAcademicYearForm(AcademicYearForm):

    def __init__(self, original_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_name = original_name

    def validate_name(self, field):

        if field.data == self.original_name:
            return

        existing = AcademicYear.query.filter_by(
            name=field.data.strip()
        ).first()

        if existing:
            raise ValidationError(
                "Academic Year already exists."
            )