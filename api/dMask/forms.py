from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo


choices = [("What was your childhood nickname?"),
           ("In what city did you meet your spouse/significant other?"),
           ("What is the name of your favorite childhood friend?"),
           ("What street did you live on in third grade?"),
           ("What is your oldest sibling’s birthday month and year? (e.g., January 1900)"),
           ("Where were you when you had your first kiss?")]


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()]) 
    password = PasswordField("Password", validators=[DataRequired(), Length(min=2, max=35)])
    submit = SubmitField("Submit")


class UpdateForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()]) 
    password = PasswordField("Password", validators=[DataRequired(), Length(min=2, max=35)])
    confirm = PasswordField("Confirm Password", validators=[DataRequired(), Length(min=2, max=35), EqualTo("password")])
    question = SelectField("Secret question", choices=choices)
    secret = StringField("Secret answer", validators=[DataRequired()])
    submit = SubmitField("Submit")


class RecoverForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    secret = StringField("Secret answer", validators=[DataRequired()])
    submit = SubmitField("Submit")


class ResetForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired(), Length(min=2, max=35)])
    confirm = PasswordField("Confirm Password", validators=[DataRequired(), Length(min=2, max=35), EqualTo("password")])
    submit = SubmitField("Submit")