from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class FacultyForm(FlaskForm):

    name = StringField(
        "Faculty Name",
        validators=[
            DataRequired(),
            Length(max=100)
        ]
    )

    code = StringField(
        "Faculty Code",
        validators=[
            DataRequired(),
            Length(max=20)
        ]
    )

    description = TextAreaField(
        "Description"
    )

    submit = SubmitField("Save Faculty")