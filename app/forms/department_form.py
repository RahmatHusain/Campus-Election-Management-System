from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    SelectField,
    BooleanField,
    SubmitField
)
from wtforms.validators import DataRequired, Length

from app.models.faculty import Faculty


class DepartmentForm(FlaskForm):

    name = StringField(
        "Department Name",
        validators=[
            DataRequired(),
            Length(max=120)
        ]
    )

    code = StringField(
        "Department Code",
        validators=[
            DataRequired(),
            Length(max=20)
        ]
    )

    faculty_id = SelectField(
        "Faculty",
        coerce=int,
        validators=[DataRequired()]
    )

    description = TextAreaField(
        "Description"
    )

    is_active = BooleanField(
        "Active",
        default=True
    )

    submit = SubmitField(
        "Save Department"
    )

    def load_faculties(self):

        self.faculty_id.choices = [

            (faculty.id, faculty.name)

            for faculty in Faculty.query
            .filter_by(is_active=True)
            .order_by(Faculty.name)
            .all()

        ]