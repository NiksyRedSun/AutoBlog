from flask import Flask, render_template, request, g, flash, abort, redirect, url_for, make_response
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from UserLogin import UserLogin
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash
from forms import LoginForm, RegisterForm, PostForm, GetCharForm, ItemsPostForm
from admin.admin import admin
from manyFunc import badlang_correct, in_web_presentation, check_sum
from models import db, addPost, addUser, getTenPosts, getUserByName, getUser, getCharacter, getCharToUser, \
    getCharacterByUserId, getStatistic, getItemsByChar, itemToForm, postItem, putItem, makeEmptyItem, getItem
from flask_migrate import Migrate


SECRET_KEY = "#asgfkjdklsfgjserutdfg-09423"
SQLALCHEMY_DATABASE_URI = "sqlite:///blog.db"


app = Flask(__name__, static_url_path='/static')
app.config.from_object(__name__)


app.register_blueprint(admin, url_prefix='/admin')
login_manager = LoginManager(app)


db.init_app(app) # вот тут мы создаем нашу бд из models
migrate = Migrate(app, db, render_as_batch=True)



login_manager.login_view = 'login'
login_manager.login_message = ""
login_manager.login_message_category = "error"



menu = [
        {"name": "Личный кабинет", "url": "profile"},
        {"name": "Регистрация", "url": "registration"},
        {"name": "Блог", "url": "index"}
        ]


@login_manager.user_loader
def load_user(user_id):
    return UserLogin().fromDB(getUser(user_id))



@app.route("/", methods=["POST", "GET"])
def index():
    posts = getTenPosts()
    if current_user.is_authenticated:
        nickname = current_user.getName()
    else:
        nickname = None
    form = PostForm()
    if form.validate_on_submit():
        posttext = form.post.data
        posttext = badlang_correct(posttext)
        if current_user.is_authenticated:
            postauthor = current_user.getName()
            res = addPost(postauthor, posttext)
        else:
            res = addPost("Anon", posttext)
        if res:
            flash("Ваш пост добавлен", "success")
            return redirect(url_for("index"))
        else:
            flash("Ошибка при добавлении поста", "error")

    return render_template("index.html", menu=menu, nickname=nickname, form=form, posts=posts)


@app.route("/registration", methods=["POST", "GET"])
def registration():
    form = RegisterForm()
    if form.validate_on_submit():
        hash = generate_password_hash(form.psw.data)
        res = addUser(form.name.data, hash)
        if res:
            flash("Вы успешно зарегистрированы", "success")
            # return redirect(url_for('profile'))
        else:
            flash("Ошибка при добавлении в БД", "error")

    return render_template("registration.html", menu=menu, form=form, title="Регистрация")



@app.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = getUserByName(form.name.data)
        if user and check_password_hash(user.psw, form.psw.data):
            userlogin = UserLogin().create(user)
            rm = form.remember.data
            login_user(userlogin, remember=rm)
            return redirect(request.args.get("next") or url_for("profile"))

        flash("Неверная пара логин/пароль", "error")

    return render_template("login.html", menu=menu, title="Авторизация", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Вы вышли из аккаунта", "success")
    return redirect(url_for("login"))



@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html", menu=menu, title="Личный кабинет")



@app.route("/profile/get_char", methods=["POST", "GET"])
@login_required
def get_char():
    form = GetCharForm()
    if form.validate_on_submit():
        char_id = form.id.data
        if not getCharacter(char_id):
            flash("Ваш персонаж не найден в базе данных", "error")
        else:
            getCharToUser(current_user.get_id(), char_id)
            flash("Все получилось", "success")
            redirect(url_for("show_char"))
    return render_template("get_char.html", menu=menu, title="Персонаж", form=form)



@app.route("/profile/show_char", methods=["POST", "GET"])
@login_required
def show_char():
    char = getCharacterByUserId(current_user.get_id())
    if not char:
        redirect(url_for("get_char"))

    items = getItemsByChar(char.id) #получаем имеющиеся вещи чара
    if char.items_available != len(items):
        for i in range(char.items_available - len(items)):
            makeEmptyItem(char.id)

    items = getItemsByChar(char.id)  #еще раз получаем их после создания, если они до этого не были созданы
    itemsIds = list(map(lambda x: x.id, items))

    stat = getStatistic(char.id)
    info = in_web_presentation(char)

    return render_template("show_char.html", menu=menu, title="Персонаж", info=info, stat=stat, char=char, itemsIds=itemsIds, length=len(itemsIds))



@app.route("/profile/show_char/item/<id>", methods=["POST", "GET"])
@login_required
def show_item(id):
    char = getCharacterByUserId(current_user.get_id())
    items = getItemsByChar(char.id)
    itemsIds = list(map(lambda x: x.id, items))

    if int(id) not in itemsIds:
        return redirect(url_for("not_your_item"))

    item = getItem(id)
    form = ItemsPostForm()

    if form.validate_on_submit():
        if check_sum(form):
            if putItem(form, item):
                flash("Вещь успешно обновлена", "success")
            else:
                flash("Что-то пошло не так", "error")
        else:
            flash("В сумме выходит больше 6и очков", "error")

    itemToForm(item, form)
    return render_template("show_item.html", menu=menu, title="Вещи", form=form)


@app.route("/not_your_item", methods=["POST", "GET"])
@login_required
def not_your_item():
    return render_template("not_item.html", menu=menu, title="Не та вещь")


if __name__ == "__main__":
    app.run(debug=True)

#
# if __name__ == "__main__":
#     app.run(host='0.0.0.0')
#
