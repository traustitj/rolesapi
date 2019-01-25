from db.db import Database

def setup():
    mydb = Database()
    mydb.get_query("drop table if exists roles", ())
    mydb.get_query("drop table if exists user_roles", ())
    mydb.get_query("drop table if exists users", ())
    mydb.set_query("CREATE TABLE if not exists users (userid integer, name varchar, username varchar, created timestamp)", ())
    mydb.set_query("CREATE TABLE if not exists user_roles (roleid integer, userid integer)", ())
    mydb.set_query("CREATE TABLE if not exists roles (id integer primary key autoincrement, name varchar, permanent byte)", ())

    mydb.set_query("insert into roles (name, permanent) values(?, ?)", ('developer', 1))
    mydb.set_query("insert into roles (name, permanent) values(?, ?)", ('Product Owner', 1))
    mydb.set_query("insert into roles (name, permanent) values(?, ?)", ('Tester', 1))

setup()