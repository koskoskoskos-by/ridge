from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, SubmitField, FloatField, IntegerField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class LoginForm(FlaskForm):
    email = StringField('Адрес электронной почты: ', validators=[Email()])
    password = PasswordField('Пароль: ', validators=[Length(min=6, max=15)])
    submit = SubmitField('Войти')


class RegistrationForm(FlaskForm):
    name = StringField('Имя пользователя', validators=[DataRequired()])
    email = StringField('Адрес электронной почты', validators=[Email()])
    password = PasswordField('Пароль: ', validators=[EqualTo('conf_password'), Length(min=6, max=15)])
    conf_password = PasswordField('Подтвердите пароль:')
    submit = SubmitField('Зарегистрироваться')


class AddProductForm(FlaskForm):
    name = StringField('Имя товара', validators=[DataRequired()])
    description = StringField('Описание товара', validators=[DataRequired()])
    price = FloatField('Цена товара',validators=[DataRequired()])
    stock_quantity = IntegerField('Количество на складе', default=0)
    image = FileField('Изображение товара',
                      validators=[FileRequired(), FileAllowed(['jpg', 'jpeg', 'png'], 'Только jpg, jpeg, png')])
    submit = SubmitField('Добавить')
