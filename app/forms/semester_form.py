from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    IntegerField,
    DateField,
    BooleanField,
    SelectField,
    SubmitField
)
from wtforms.validators import DataRequired, NumberRange

from app.models.academic_year import AcademicYear
from app.models.semester import Semester


class SemesterForm(FlaskForm):

    academic_year_id = SelectField(
        'Academic Year',
        coerce=int,
        validators=[DataRequired()]
    )

    name = StringField(
        'Semester Name',
        validators=[DataRequired()]
    )

    semester_number = IntegerField(
        'Semester Number',
        validators=[
            DataRequired(),
            NumberRange(min=1, max=16)
        ]
    )

    start_date = DateField(
        'Start Date',
        validators=[DataRequired()]
    )

    end_date = DateField(
        'End Date',
        validators=[DataRequired()]
    )

    is_current = BooleanField('Current Semester')
    is_active = BooleanField('Active', default=True)

    submit = SubmitField('Save Semester')

    # -----------------------------
    # IMPORTANT FIX
    # -----------------------------
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        # Load academic years for dropdown
        self.academic_year_id.choices = [

            (y.id, y.name)

            for y in AcademicYear.query.order_by(
                AcademicYear.start_date.desc()
            ).all()

        ]
# ==========================================
# Edit Semester Form
# ==========================================

class EditSemesterForm(SemesterForm):

    def __init__(self, original_name, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.original_name = original_name

    def validate_name(self, field):

        # Allow same name when editing
        if field.data.strip() == self.original_name.strip():
            return

        existing = Semester.query.filter_by(
            academic_year_id=self.academic_year_id.data,
            name=field.data.strip()
        ).first()

        if existing:

            raise ValidationError(
                'Semester already exists in this academic year.'
            )