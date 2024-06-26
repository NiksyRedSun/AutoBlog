from flask_login import UserMixin
from flask import url_for


class UserLogin(UserMixin):
    def fromDB(self, user):
        self.__user = user
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
        return self.__user.id


    def getName(self):
        return self.__user.name if self.__user else "Без имени"

    def getHash(self):
        return self.__user.psw[0:40] if self.__user else "Без HASH????"

