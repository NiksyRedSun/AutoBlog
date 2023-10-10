from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange


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


class GetCharForm(FlaskForm):
    id = IntegerField("ID персонажа", validators=[DataRequired()])
    submit = SubmitField("Подключить персонажа")


def DeletePostsForm(posts):
    class DeletePostForm(FlaskForm):
        pass

    DeletePostForm.submit = SubmitField("Удалить посты")
    ids = {}
    for post in posts:
        ids["id" + str(post.id)] = post.id
        postname = f"ID поста: {post.id} Автор: {post.usr}\n Текст: {post.text}"
        setattr(DeletePostForm, "id" + str(post.id), BooleanField(postname, default=False))

    form = DeletePostForm()
    return form, ids


def ItemsPostForm(num):
    class ItemsPostForm(FlaskForm):
        pass

    ItemsPostForm.submit = SubmitField("Обновить вещи")
    setattr(ItemsPostForm, "itemNum", num)
    for i in range(1, num+1):
        setattr(ItemsPostForm, f"itemName{i}", StringField(f"Название вещи {i}", validators=[Length(min=4, max=100, message="Должно быть от 4 до 100 символов")]))
        setattr(ItemsPostForm, f"itemMaxHp{i}", IntegerField(f"Подъем hp", validators=[NumberRange(min=0, message="Не должно быть меньше 0")]))
        setattr(ItemsPostForm, f"itemAttack{i}", IntegerField(f"Подъем атаки", validators=[NumberRange(min=0, message="Не должно быть меньше 0")]))
        setattr(ItemsPostForm, f"itemDefense{i}", IntegerField(f"Подъем защиты", validators=[NumberRange(min=0, message="Не должно быть меньше 0")]))
        setattr(ItemsPostForm, f"itemInitiative{i}", IntegerField(f"Подъем ловкости", validators=[NumberRange(min=0, message="Не должно быть меньше 0")]))
        setattr(ItemsPostForm, f"forAttack{i}", BooleanField(f"Используется для атаки", default=False))

    form = ItemsPostForm()
    return form