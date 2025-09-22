from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField,SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class LoginForm(FlaskForm):
    email = StringField('Адрес электронной почты: ', validators=[Email()])
    password = PasswordField('Пароль: ', validators=[Length(min=6, max=15)])
    submit = SubmitField('Войти')


class RegistrationForm(FlaskForm):
    name = StringField('Имя пользователя', validators=[DataRequired()])
    email = StringField('Адрес электронной почты', validators=[Email()])
    password = PasswordField('Пароль: ', validators=[EqualTo('conf_password'),Length(min=6, max=15)])
    conf_password = PasswordField('Подтвердите пароль:')
    submit = SubmitField('Зарегистрироваться')

