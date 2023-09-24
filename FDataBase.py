import math
import sqlite3
import time
from manyFunc import tmstp_to_str

class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()


    def getMenu(self):
        sql = '''SELECT * FROM mainmenu'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res:
                return res
        except:
            print("Ошибка чтения из БД")
        return []


    def addPost(self, author, text):
        try:
            tm = math.floor(time.time())
            self.__cur.execute("INSERT INTO posts VALUES (NULL, ?, ?, ?)", (author, text, tm))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления статьи в БД" + str(e))
            return False
        return True

    def getPost(self, alias):
        try:
            self.__cur.execute(f"SELECT title, text FROM posts WHERE url LIKE '{alias}' LIMIT 1")
            res = self.__cur.fetchone()
            if res:
                return res
        except sqlite3.Error as e:
            print("Ошибка получения статьи из БД " + str(e))


        print(False, False)


    def getPostsAnonce(self):
        try:
            self.__cur.execute(f"SELECT id, title, text, url FROM posts ORDER BY time DESC")
            res = self.__cur.fetchall()
            if res:
                return res
        except sqlite3.Error as e:
            print("Ошибка получения информации из бд" + str(e))

        return []


    def getTenPosts(self):
        try:
            self.__cur.execute(f"SELECT id, usr, text, time FROM posts ORDER BY id DESC")
            res = self.__cur.fetchall()
            res = list(map(lambda item: {k: (item[k] if k!="time" else tmstp_to_str(item[k])) for k in item.keys()}, res)) #а вот разберись что тут происходит, если ты такой умный
            if res:
                return res[0:10]
        except sqlite3.Error as e:
            print("Ошибка получения информации из бд" + str(e))

        return []


    def getAllPosts(self):
        try:
            self.__cur.execute(f"SELECT id, usr, text, time FROM posts ORDER BY id DESC")
            res = self.__cur.fetchall()
            res = list(map(lambda item: {k: (item[k] if k!="time" else tmstp_to_str(item[k])) for k in item.keys()}, res)) #а вот разберись что тут происходит, если ты такой умный
            if res:
                return res
        except sqlite3.Error as e:
            print("Ошибка получения информации из бд" + str(e))

        return []


    def addUser(self, name, hpsw):
        try:
            self.__cur.execute(f"SELECT COUNT() as `count` FROM users WHERE name LIKE '{name}'")
            res = self.__cur.fetchone()
            if res["count"] > 0:
                print("Пользователь с таким именем уже существует")
                return False

            self.__cur.execute(f"INSERT INTO users VALUES(NULL, ?, ?)", (name, hpsw))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления пользователя в БД " + str(e))
            return False

        return True


    def getUser(self, user_id):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE id = {user_id} LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False

            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из бд" + str(e))

        return False


    def getAllUsers(self):
        try:
            self.__cur.execute(f"SELECT * FROM users")
            res = self.__cur.fetchall()

            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из бд" + str(e))

        return False



    def getUserByName(self, name):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE name = '{name}' LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False

            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из бд" + str(e))

        return False


    def updateUserAvatar(self, avatar, user_id):
        if not avatar:
            return False

        try:
            binary = sqlite3.Binary(avatar)
            self.__cur.execute(f"UPDATE users SET avatar = ? WHERE id = ?", (binary, user_id))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка обновления аватара" + str(e))
            return False
        return True