from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo
from flask_wtf.file import FileField, FileAllowed

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4)])
    submit = SubmitField('Login')

class PhotoUploadForm(FlaskForm):
    photo = FileField('Завантажте фото', validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Дозволено завантажувати лише фотографії.')])
    submit = SubmitField('Завантажити')

class ChangeLoginPasswordForm(FlaskForm):
    new_login = StringField('Новий логін', validators=[DataRequired()])
    new_password = PasswordField('Новий пароль', validators=[DataRequired()])
    submit = SubmitField('Змінити логін та пароль')

