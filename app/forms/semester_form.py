from datetime import date

from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SelectField,
    IntegerField,
    DateField,
    BooleanField,
    SubmitField
)
from wtforms.validators import (
    DataRequired,
    Length,
    NumberRange,
    ValidationError
)

from app.models.academic_year import AcademicYear
from app.models.semester import Semester


class SemesterForm(FlaskForm):

    academic_year_id = SelectField(
        "Academic Year",
        coerce=int,
        validators=[DataRequired()]
    )

    name = StringField(
        "Semester Name",
        validators=[
            DataRequired(),
            Length(min=3, max=50)
        ]
    )

    semester_number = IntegerField(
        "Semester Number",
        validators=[
            DataRequired(),
            NumberRange(min=1, max=12)
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
        "Set as Current Semester"
    )

    is_active = BooleanField(
        "Active",
        default=True
    )

    submit = SubmitField("Save Semester")

    def __init__(self, original_id=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.original_id = original_id

        self.academic_year_id.choices = [
            (year.id, year.name)
            for year in AcademicYear.query.order_by(
                AcademicYear.start_date.desc()
            ).all()
        ]

    def validate_name(self, field):

        query = Semester.query.filter_by(
            academic_year_id=self.academic_year_id.data,
            name=field.data.strip()
        )

        if self.original_id:
            query = query.filter(Semester.id != self.original_id)

        if query.first():
            raise ValidationError(
                "Semester name already exists for this Academic Year."
            )

    def validate_semester_number(self, field):

        query = Semester.query.filter_by(
            academic_year_id=self.academic_year_id.data,
            semester_number=field.data
        )

        if self.original_id:
            query = query.filter(Semester.id != self.original_id)

        if query.first():
            raise ValidationError(
                "Semester number already exists."
            )

    def validate_end_date(self, field):

        if field.data <= self.start_date.data:
            raise ValidationError(
                "End Date must be after Start Date."
            )

    def validate_start_date(self, field):

        if field.data < date(2000, 1, 1):
            raise ValidationError(
                "Invalid Start Date."
            )