import sqlite3

from flask import Blueprint, render_template, request, g, flash, abort, redirect, url_for, make_response, session
from forms import LoginForm, RegisterForm, PostForm

admin = Blueprint('admin', __name__, template_folder="templates", static_folder="static")
from FDataBase import FDataBase



def login_admin():
    session['admin_logged'] = 1


def isLogged():
    return True if session.get("admin_logged") else False


def logout_admin():
    session.pop("admin_logged", None)


menu = [
        {"name": "Личный кабинет", "url": "profile"},
        {"name": "Регистрация", "url": "registration"},
        {"name": "Блог", "url": "/"}
        ]



dbase = None
@admin.before_request
def before_request():
    global dbase
    db = g.get("link_db")
    dbase = FDataBase(db)


@admin.teardown_request
def teardown_request(request):
    global dbase
    dbase = None
    return request



@admin.route("/")
def index():
    if not isLogged():
        return redirect(url_for(".login"))

    return render_template('admin/index.html', menu=menu, title='Админ-панель')



@admin.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if isLogged():
        return redirect(url_for('.index'))
    if form.validate_on_submit():
        if form.name.data == "admin" and form.psw.data == "tvoyamamasha228":
            login_admin()
            return redirect(url_for('.index'))
        else:
            flash("Неверная пара логин/пароль", "error")

    return render_template("admin/login.html", title='Вход в личный кабинет администратора', form=form, menu=menu)



@admin.route("/logout", methods=["POST", "GET"])
def logout():
    if not isLogged():
        return redirect(url_for('.login'))

    logout_admin()

    return redirect(url_for('.login'))



@admin.route("/list-pubs")
def listpubs():
    if not isLogged():
        return redirect(url_for('.login'))

    posts = dbase.getAllPosts()
    return render_template("admin/list-pubs.html", title="Список статей", menu=menu, posts=posts)



@admin.route("/list-users")
def listusers():
    if not isLogged():
        return redirect(url_for('.login'))

    users = dbase.getAllUsers()
    return render_template("admin/list-users.html", title="Список пользователей", menu=menu, users=users)