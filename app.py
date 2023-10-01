from flask import Flask, render_template, request, g, flash, abort, redirect, url_for, make_response
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from UserLogin import UserLogin
import sqlite3
import os
from FDataBase import FDataBase
from werkzeug.security import generate_password_hash, check_password_hash
from forms import LoginForm, RegisterForm, PostForm
from admin.admin import admin
from manyFunc import badlang_correct
from flask_sqlalchemy import SQLAlchemy
import sqlam
import time, math
from datetime import datetime



# DATABASE = '/tmp/flsite.db'
SECRET_KEY = "#asgfkjdklsfgjserutdfg-09423"
SQLALCHEMY_DATABASE_URI = "sqlite:///blog.db"


app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flsite.db')))

app.register_blueprint(admin, url_prefix='/admin')
login_manager = LoginManager(app)

db = SQLAlchemy(app)

#все это будет здесь, пока я не разберусь, куда это лучше засунуть


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    psw = db.Column(db.String(500), nullable=True)

    def __repr__(self):
        return f"user_id: {self.id}, user_name: {self.name}"


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usr = db.Column(db.String(50))
    text = db.Column(db.Text, nullable=True)
    time = db.Column(db.DateTime)

    def __repr__(self):
        return f"post_id: {self.id}, post_author: {self.usr}, post_time: {str(self.time)}"


def addUser(name, hash):
    try:
        u = Users(name=name, psw=hash)
        db.session.add(u) #добавляет запись в сессию
        db.session.flush() #перемещает запись из сессии в таблицу
        db.session.commit()
        return True
    except:
        db.session.rollback()
        print("Что-то пошло не так при добавлении пользователя в бд")


def addPost(postauthor, posttext):
    # try:
        p = Posts(usr=postauthor, text=posttext, time=datetime.now())
        db.session.add(p) #добавляет запись в сессию
        db.session.flush() #перемещает запись из сессии в таблицу
        db.session.commit()
        return True
    # except:
    #     db.session.rollback()
    #     print("Что-то пошло не так при добавлении поста")


def getTenPosts():
    try:
        result = Posts.query.all()[0:10]
        result.reverse()
        return result
    except:
        print("Что-то пошло не так при загрузке постов")


def getUserByName(name):
    try:
        u = Users.query.filter_by(name=name)[0]
        return u
    except:
        print("Что-то пошло не так при загрузке пользователя")


def getUser(user_id):
    try:
        res = Users.query.filter_by(id=user_id)[0]
        if not res:
            print("Пользователь не найден")
            return False

        return res
    except sqlite3.Error as e:
        print("Ошибка получения данных из бд" + str(e))


#пока что не трогаем этот раздел


login_manager.login_view = 'login'
login_manager.login_message = ""
login_manager.login_message_category = "error"



menu = [
        {"name": "Личный кабинет", "url": "profile"},
        {"name": "Регистрация", "url": "registration"},
        {"name": "Блог", "url": "/"}
        ]


@login_manager.user_loader
def load_user(user_id):
    return UserLogin().fromDB(getUser(user_id))


# def connect_db():
#     conn = sqlite3.connect(app.config['DATABASE'])
#     conn.row_factory = sqlite3.Row
#     return conn
#
#
# def create_db():
#     db = connect_db()
#     with app.open_resource("sq_db.sql", mode="r") as f:
#         db.cursor().executescript(f.read())
#     db.commit()
#     db.close()
#
# def get_db():
#     if not hasattr(g, 'link_db'):
#         g.link_db = connect_db()
#     return g.link_db



# dbase = None

# @app.before_request
# def befor_request():
#     global dbase
#     db = get_db()
#     dbase = FDataBase(db)



# @app.teardown_appcontext
# def close_db(error):
#     if hasattr(g, 'link_db'):
#         g.link_db.close()




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
    if current_user.is_authenticated:
        return render_template("profile.html", menu=menu, title="Личный кабинет")
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
# print(type(time.time()))

#
#
# if __name__ == "__main__":
#     app.run(host='0.0.0.0')