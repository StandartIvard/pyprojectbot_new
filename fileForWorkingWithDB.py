import sqlite3
import hashlib


def getInformVK(id):
    con = sqlite3.connect('DBuser.db')
    cur = con.cursor()
    print(str(id))
    return cur.execute("SELECT * FROM users WHERE vkid = '" + str(id) + "';").fetchall()


def getInformDiscord(id):
    con = sqlite3.connect('DBuser.db')
    cur = con.cursor()
    print(str(id))
    return cur.execute("SELECT * FROM users WHERE dsid = '" + str(id) + "';").fetchall()


def insertVK(name, id):
    con = sqlite3.connect('DBuser.db')
    cur = con.cursor()
    cur.execute("INSERT INTO users(name,vkid) VALUES('" + name + "','" + id + "')")
    con.commit()


def SetDiscord(name, id):
    con = sqlite3.connect('DBuser.db')
    cur = con.cursor()
    cur.execute("UPDATE users SET disid = '" + id + "' WHERE name = '" + name + "';")
    con.commit()


def VKpass(password, id):
    con = sqlite3.connect('DBuser.db')
    cur = con.cursor()
    password = hashlib.md5(bytes(password, encoding='utf8'))
    p = password.hexdigest()
    cur.execute("UPDATE users SET password = '" + str(p) + "' WHERE vkid = '" + str(id) + "';")
    con.commit()


def getInformTG(id):
    con = sqlite3.connect('DBuser.db')
    cur = con.cursor()
    print(str(id))
    return cur.execute("SELECT * FROM users WHERE tgid = '" + str(id) + "';").fetchall()


def TGid(tgid, id):
    con = sqlite3.connect('DBuser.db')
    cur = con.cursor()
    cur.execute("UPDATE users SET tgid = '" + str(tgid) + "' WHERE vkid = '" + str(id) + "';")
    con.commit()


def SetPassword(name, password):
    con = sqlite3.connect('DBuser.db')
    cur = con.cursor()
    p = password.hexdigest()
    cur.execute("UPDATE users SET password = '" + str(p) + "' WHERE name = '" + name + "';")
    con.commit()


def getInformAll():
    con = sqlite3.connect('DBuser.db')
    cur = con.cursor()
    return cur.execute("SELECT * FROM users").fetchall()


con = sqlite3.connect('DBuser.db')
cur = con.cursor()
print(cur.execute("SELECT * FROM users").fetchall())