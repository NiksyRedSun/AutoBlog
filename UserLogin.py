from flask_login import UserMixin
from flask import url_for


class UserLogin(UserMixin):
    def fromDB(self, user_id, db):
        self.__user = db.getUser(user_id)
        return self

#Класс создан таким образом, что в переменной __user хранится вся информация о пользователе из БД

    def create(self, user):
        self.__user = user
        return self

    # def is_authenticated(self): #эти методы наследуются от UserMixin
    #     return True
    #
    # def is_active(self):
    #     return True
    #
    # def is_anonymous(self):
    #     return False

    def get_id(self):
        return str(self.__user['id'])


    def getName(self):
        return self.__user["name"] if self.__user else "Без имени"

    def getHash(self):
        return self.__user["psw"][0:40] if self.__user else "Без HASH????"


    def getAvatar(self, app):
        img = None
        if not self.__user['avatar']:
            try:
                with app.open_resource(app.root_path + url_for("static", filename="images/default.png"), "rb") as f:
                    img = f.read()
            except FileNotFoundError as e:
                print("Не найден аватар по умолчанию" + str(e))
        else:
            img = self.__user['avatar']

        return img

    def verifyExt(self, filename):
        ext = filename.rsplit(".", 1)[1]
        if ext == "png" or ext == "PNG":
            return True
        return False