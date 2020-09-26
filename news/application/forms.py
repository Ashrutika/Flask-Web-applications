from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from application.models import User

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()],)
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6,max=15)])
    remember_me = BooleanField("Remember me")
    login = SubmitField("Login")

class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6,max=15)])
    password_confirm = PasswordField("Confirm Password", validators=[DataRequired(), Length(min=6,max=15), EqualTo('password')])
    language = SelectField(u'Programming Language', choices=[('select', 'Select account type'),('guest', 'Guest'), ('user', 'User')],validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired(), Length(min=3,max=55)])
    signup = SubmitField("Register Now")

    def validate_email(self,email):
        user = User.objects(email=email.data).first()
        if user:
            raise ValidationError("Email is already in use. Pick another one.")

class AddNews(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    headline = StringField("Headline", validators=[DataRequired()])
    description = TextAreaField("Description",validators=[DataRequired()])
    add= SubmitField("Add")