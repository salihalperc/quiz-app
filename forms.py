from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField
from wtforms.validators import DataRequired

class QuizForm(FlaskForm):
    name = StringField("Adınız:", validators=[DataRequired()])
    submit = SubmitField("Gönder")
