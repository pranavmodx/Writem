from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextField, TextAreaField, DateField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError
from flask_app.models import User, Todo, Blog
from flask_login import current_user


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
                             DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already exists.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
                             DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user == None:
            raise ValidationError("Account doesn't exist with that email.")

    # def validate_password(self, password):
    #     user = User.query.filter_by(password=password.data).first()
    #     if user == None:
    #         raise ValidationError("Password is incorrect.")


class TodoForm(FlaskForm):
    title = TextField('Todo', validators=[DataRequired()])
    desc = TextAreaField('Description')
    submit = SubmitField('Add')

    # def validate_title(self, title):
    #     titles = Todo.query.filter_by(title=title.data).all()
    #     for title in titles:
    #         if title.user == current_user:
    #             raise ValidationError('That task already exists. Finish it')


class BlogForm(FlaskForm):
    title = TextField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')

    # def validate_title(self, title):
    #     titles = Blog.query.filter_by(title=title.data).all()
    #     for title in titles:
    #         if title.user == current_user:
    #             raise ValidationError('A blog post with that same title already exists!')


class DateForm(FlaskForm):
    date = DateField('Choose Date', validators=[DataRequired()], format = '%d/%m/%Y', description = 'Pick a date to see an interesting fact')
    submit = SubmitField('Tap')