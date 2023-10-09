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



class Characters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    story = db.Column(db.Text)
    hp = db.Column(db.Integer)
    max_hp = db.Column(db.Integer)
    attack = db.Column(db.Integer)
    defense = db.Column(db.Integer)
    initiative = db.Column(db.Integer)
    points = db.Column(db.Integer)
    money = db.Column(db.Integer)
    level = db.Column(db.Integer)
    exp = db.Column(db.Integer)
    next_level_exp = db.Column(db.Integer)
    autosave = db.Column(db.Boolean, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    def __repr__(self):
        return f"Char id: {self.id}, char name: {self.name}"




class Statistics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mobKill = db.Column(db.Integer)
    bossKill = db.Column(db.Integer)
    death = db.Column(db.Integer)
    itemsUsed = db.Column(db.Integer)
    moneySpend = db.Column(db.Integer)
    fountainHealing = db.Column(db.Integer)
    hits = db.Column(db.Integer)
    criticalHits = db.Column(db.Integer)
    successAvoiding = db.Column(db.Integer)
    leavingBossFights = db.Column(db.Integer)
    leavingMobFights = db.Column(db.Integer)
    char_id = db.Column(db.Integer, db.ForeignKey("characters.id"), nullable=True)

    def __repr__(self):
        return f"Stat id: {self.id}, char id: {self.char_id}"


def getStatistic(char_id):
    try:
        s = Statistics.query.filter_by(char_id=char_id).first()
        if not s:
            print("Статистика не найдена")
            return False
        return s
    except:
        print("Что-то пошло не так при загрузке статистики")




def getCharacter(char_id):
    try:
        u = Characters.query.get(char_id)
        if not u:
            print("Пользователь не найден")
            return False
        return u
    except:
        print("Что-то пошло не так при загрузке пользователя")


def getCharToUser(id, char_id):
    with db.session() as s:
        try:
            u = Characters.query.get(char_id)
            u.user_id = id
            s.commit()
            return u
        except:
            print("Что-то пошло не так при загрузке пользователя")


def getCharacterByUserId(user_id):
    try:
        u = Characters.query.filter_by(user_id=user_id).first()
        if not u:
            print("Пользователь не найден")
            return False
        return u
    except:
        print("Что-то пошло не так при загрузке пользователя")


def addUser(name, hash):
    with db.session() as s:
        try:
            u = Users(name=name, psw=hash)
            s.add(u) #добавляет запись в сессию
            s.flush() #перемещает запись из сессии в таблицу
            s.commit()
            return True
        except:
            db.session.rollback()
            print("Что-то пошло не так при добавлении пользователя в бд")



def addPost(postauthor, posttext):
    with db.session() as s:
        try:
            p = Posts(usr=postauthor, text=posttext, time=datetime.now(), string_time=datetime.now().strftime("%H:%M %d.%m.%Y"))
            s.add(p) #добавляет запись в сессию
            s.flush() #перемещает запись из сессии в таблицу
            s.commit()
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
        u = Users.query.get(user_id)
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