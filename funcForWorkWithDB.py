import sqlite3
import hashlib


def getInformDB(name):
    con = sqlite3.connect('userDB.db')
    cur = con.cursor()
    return cur.execute("SELECT * FROM users WHERE name = '" + name + "'").fetchall()


def insertVK(name, id):
    con = sqlite3.connect('userDB.db')
    cur = con.cursor()
    cur.execute("INSERT INTO users(name,id) VALUES('" + name + "','" + id + "')")
    con.commit()


def VKpass(password, id):
    con = sqlite3.connect('userDB.db')
    cur = con.cursor()
    password = hashlib.md5(bytes(password, encoding='utf8'))
    p = password.hexdigest()
    cur.execute("UPDATE users SET password = '" + str(p) + "' WHERE vkid = '" + str(id) + "';")
    con.commit()


def SetPassword(name, password):
    con = sqlite3.connect('userDB.db')
    cur = con.cursor()
    p = password.hexdigest()
    cur.execute("UPDATE users SET password = '" + str(p) + "' WHERE name = '" + name + "';")
    con.commit()

con = sqlite3.connect('userDB.db')
cur = con.cursor()
print(cur.execute("SELECT * FROM users").fetchall())