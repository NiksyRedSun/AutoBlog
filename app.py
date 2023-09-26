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



DATABASE = '/tmp/flsite.db'
SECRET_KEY = "#asgfkjdklsfgjserutdfg-09423"

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flsite.db')))

app.register_blueprint(admin, url_prefix='/admin')
login_manager = LoginManager(app)


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
    print("load_user")
    return UserLogin().fromDB(user_id, dbase)


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def create_db():
    db = connect_db()
    with app.open_resource("sq_db.sql", mode="r") as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()

def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db



dbase = None

@app.before_request
def befor_request():
    global dbase
    db = get_db()
    dbase = FDataBase(db)



@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()




@app.route("/", methods=["POST", "GET"])
def index():
    posts = dbase.getTenPosts()
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
            res = dbase.addPost(postauthor, posttext)
        else:
            res = dbase.addPost("Anon", posttext)
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
        res = dbase.addUser(form.name.data, hash)
        if res:
            flash("Вы успешно зарегистрированы", "success")
            return redirect(url_for('profile'))
        else:
            flash("Ошибка при добавлении в БД", "error")

    return render_template("registration.html", menu=menu, form=form, title="Регистрация")



@app.route("/login", methods=["POST", "GET"])
def login():
    # if current_user.is_authenticated:
    #     return redirect(url_for("profile"))
    form = LoginForm()
    print(form.remember)
    if form.validate_on_submit():
        user = dbase.getUserByName(form.name.data)
        if user and check_password_hash(user['psw'], form.psw.data):
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


#
#
# if __name__ == "__main__":
#     app.run(host='0.0.0.0')