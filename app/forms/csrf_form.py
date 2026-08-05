from flask_wtf import FlaskForm
from wtforms import SubmitField


class CandidateActionForm(FlaskForm):
    submit = SubmitField("Confirm")