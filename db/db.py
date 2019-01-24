import os
import sqlite3
import time
from models import User, Role

class Database():
    connection = None
    PATH = os.path.join(os.path.dirname(__file__), 'database.sqlite')
    def __init__(self):
        self.connection = sqlite3.connect(self.PATH)
        print(self.PATH)

    def test(self):
        cursor = self.connection.cursor()
        cursor.execute("select * from test")

        return cursor.fetchall()

    def save_user(self, user):
        cursor = self.connection.cursor()
        cursor.execute('insert into users (userid, username, name, created) values (?, ?, ?, ?)', (user["id"], user["username"], user["name"], time.time()))
        self.connection.commit()
        
        user = self.get_user(user["id"])

        return user

    def get_user(self, userid):
        userid = "%s" % (userid)
        cursor = self.connection.cursor()
        cursor.execute("select userid, username, name, created from users where userid=?", (userid,))
        users = cursor.fetchall()
        if len(users) > 0:
            u = self._user_object(users[0])
            return u
        else:
            return None

    def create_role(self, role_name):
        if self.role_exists(role_name):
            return None
        else:
            cursor = self.connection.cursor()
            cursor.execute("insert into roles (name, permanent) values (?, ?)", (role_name.upper(), False))
            self.connection.commit()

            cursor.execute("select id, name, permanent from roles where name like upper(?)", (role_name, ))
            roles = cursor.fetchall()

            if (len(roles) > 0):
                r = self._role_object(roles[0])
                return r

    def delete_role(self, role_name):
        if self.role_exists(role_name):
            cursor = self.connection.cursor()
            role = self.get_role_by_name(role_name)
            if role.permanent == False:
                cursor.execute("delete from roles where name like upper(?)", (role_name, ))
                self.connection.commit()
                return True
        return False

    def get_role_by_name(self, role_name):
        cursor = self.connection.cursor()
        cursor.execute("select id, name, permanent from roles where name like upper(?)", (role_name, ))
        roles = cursor.fetchall()
        if len(roles) > 0:
            role = self._role_object(roles[0])
            return role

        return None

    def role_exists(self, role_name):
        cursor = self.connection.cursor()
        cursor.execute("select id, name, permanent from roles where name like upper(?)", (role_name, ))
        roles = cursor.fetchall()

        return len(roles) > 0

    def is_user_part_of_role(self, userid = 0, roleid = 0):
        cursor = self.connection.cursor()
        cursor.execute("select userid, roleid from user_roles where userid=? and roleid=?", (userid, roleid))
        data = cursor.fetchall()

        return len(data) > 0

    def __del__(self):
        self.connection.close()

    def _user_object(self, user_tuple):
        u = User()
        u.user_id = user_tuple[0]
        u.username = user_tuple[1]
        u.name = user_tuple[2]
        u.created = user_tuple[3]

        return u

    def _role_object(self, role_tuple):
        r = Role()
        r.roleid = role_tuple[0]
        r.name = role_tuple[1]
        r.permanent = role_tuple[2]

        return r