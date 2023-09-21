from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class LoginForm(FlaskForm):
    name = StringField("Логин: ", validators=[Length(min=4, max=100, message="Должен быть от 4 до 100 символов")])
    psw = PasswordField("Пароль: ", validators=[DataRequired(), Length(min=4, max=100, message="Пароль должен быть от 4 до 100 символов")])
    remember = BooleanField("Запомнить: ", default=False)
    submit = SubmitField("Войти")


class RegisterForm(FlaskForm):
    name = StringField("Логин: ", validators=[Length(min=4, max=100, message="Должен быть от 4 до 100 символов")])
    # email = StringField("Email: ", validators=[Email("Некорректный email")])
    psw = PasswordField("Пароль: ", validators=[DataRequired(), Length(min=4, max=100, message="Пароль должен быть от 4 до 100 символов")])
    psw2 = PasswordField("Пароль повторно: ", validators=[DataRequired(), EqualTo("psw", message="Пароли не совпадают")])
    submit = SubmitField("Регистрация")


class PostForm(FlaskForm):
    post = TextAreaField("Поле", validators=[Length(min=30, max=300, message="Должен быть от 30 до 300 символов")])
    submit = SubmitField("Загрузить")

