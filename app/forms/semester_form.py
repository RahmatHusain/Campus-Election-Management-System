from datetime import date

from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    IntegerField,
    SelectField,
    DateField,
    BooleanField,
    SubmitField
)
from wtforms.validators import (
    DataRequired,
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
        validators=[DataRequired()]
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

    is_current = BooleanField("Current Semester")

    is_active = BooleanField(
        "Active",
        default=True
    )

    submit = SubmitField("Save")

    def validate_end_date(self, field):

        if field.data <= self.start_date.data:
            raise ValidationError(
                "End Date must be after Start Date."
            )

    def validate_semester_number(self, field):

        semester = Semester.query.filter_by(
            academic_year_id=self.academic_year_id.data,
            semester_number=field.data
        ).first()

        if semester:
            raise ValidationError(
                "Semester Number already exists for this Academic Year."
            )

    def validate_start_date(self, field):

        year = AcademicYear.query.get(
            self.academic_year_id.data
        )

        if not year:
            return

        if field.data < year.start_date:

            raise ValidationError(
                "Semester cannot start before Academic Year."
            )

    def validate_semester_number(self, field):
        existing = Semester.query.filter_by(
            academic_year_id=self.academic_year.data,
            semester_number=field.data
            ).first()

        if existing:
            raise ValidationError(
                "Semester Number already exists for this Academic Year."
            )
    def validate_name(self, field):

        existing = Semester.query.filter_by(
            academic_year_id=self.academic_year.data,
            name=field.data.strip()
        ).first()

        if existing:
            raise ValidationError(
                "Semester already exists."
            )

    def validate_end_date(self, field):

        if field.data <= self.start_date.data:

            raise ValidationError(
                "End Date must be greater than Start Date."
            )

    def validate_start_date(self, field):

        if (
            self.end_date.data and
            (self.end_date.data - field.data).days > 366
        ):

            raise ValidationError(
                "Semester duration cannot exceed one year."
            )

    def validate(self, extra_validators=None):

        if not super().validate(extra_validators):
            return False

        year = AcademicYear.query.get(
            self.academic_year_id.data
        )

        if year:

            if self.end_date.data > year.end_date:

                self.end_date.errors.append(
                    "Semester cannot end after Academic Year."
                )

                return False

        return True