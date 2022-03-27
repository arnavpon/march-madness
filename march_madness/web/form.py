from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, NumberRange, Regexp


class TeamForm(FlaskForm):
    team = StringField("Team: ", validators=[DataRequired()])
    submit = SubmitField("Lookup team")


class SeedForm(FlaskForm):
    seed = StringField("Seed: ", validators=[DataRequired()])
    submit = SubmitField("Lookup seed")

    def validate_seed(form, field):
        # this validator will be automatically called on field
        data = form.data['seed']  # get seed input from data
        try:
            s = int(data)
            if s <= 0 or s > 16:
                raise ValidationError("Seed should be between 1 and 16")
        except ValueError:
            raise ValidationError("Please enter a number")