from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()


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
    string_time = db.Column(db.String(50))

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
    try:
        p = Posts(usr=postauthor, text=posttext, time=datetime.now(), string_time=datetime.now().strftime("%H:%M %d.%m.%Y"))
        db.session.add(p) #добавляет запись в сессию
        db.session.flush() #перемещает запись из сессии в таблицу
        db.session.commit()
        return True
    except:
        db.session.rollback()
        print("Что-то пошло не так при добавлении поста")


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
        u = Users.query.filter_by(id=user_id)[0]
        if not u:
            print("Пользователь не найден")
            return False
        return u
    except:
        print("Что-то пошло не так при загрузке пользователя")



def getAllPosts():
    try:
        result = Posts.query.all()
        result.reverse()
        return result
    except:
        print("Что-то пошло не так при загрузке постов")


def deletePosts(form, ids):
    try:
        for id in ids:
            if form.__getattribute__(id).data:
                Posts.query.filter_by(id=ids[id]).delete()
        db.session.commit()
    except:
        print("Что-то пошло не так при удалении постов")


def getAllUsers():
    try:
        result = Users.query.all()
        return result
    except:
        print("Что-то пошло не так при загрузке пользователей")