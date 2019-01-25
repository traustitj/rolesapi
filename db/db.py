import os
import sqlite3
import time
from models import User, Role

class Database():
    connection = None
    PATH = os.path.join(os.path.dirname(__file__), 'database.sqlite')
    def __init__(self):
        self.connection = sqlite3.connect(self.PATH)

    def get_query(self, query, parameters):
        cursor = self.connection.cursor()
        cursor.execute(query, parameters)

        return cursor.fetchall()

    def set_query(self, query, parameters):
        cursor = self.connection.cursor()
        cursor.execute(query, parameters)
        self.connection.commit()

    def get_roles(self):
        roles = self.get_query("select id, name, permanent from roles", ())
        ret = []
        for role in roles:
            data = self._role_object(role)
            ret.append(data.to_dict())

        return ret

    def save_user(self, user):
        self.set_query('insert into users (userid, username, name, created) values (?, ?, ?, ?)', (user["id"], user["username"], user["name"], time.time()))
        
        user = self.get_user_by_id(user["id"])

        return user

    def get_user_by_id(self, user_id):
        user_id = "%s" % (user_id)
        users = self.get_query("select userid, username, name, created from users where userid=?", (user_id,))
        if len(users) > 0:
            u = self._user_object(users[0])
            u.roles = self.get_roles_for_user(u.user_id)
            return u
        else:
            return None

    def create_role(self, role_name):
        if self.role_exists(role_name):
            return None
        else:
            self.set_query("insert into roles (name, permanent) values (?, ?)", (role_name.upper(), False))
            roles = self.get_query("select id, name, permanent from roles where name like upper(?)", (role_name, ))

            if (len(roles) > 0):
                r = self._role_object(roles[0])
                return r

    def delete_role_by_name(self, role_name):
        if self.role_exists(role_name):
            role = self.get_role_by_name(role_name)
            if role.permanent == False:
                self.set_query("delete from roles where name like upper(?)", (role_name, ))
                self.set_query("delete from user_roles where roleid=?", (role.role_id,))
                return True
        return False

    def delete_role_by_id(self, role_id):
        if self.role_id_exists(role_id):
            role = self.get_role_by_id(role_id)
            if role.permanent == False:
                self.set_query("delete from roles where id=?", (role_id, ))
                self.set_query("delete from user_roles where roleid=?", (role.role_id,))
                return True
        return False

    def get_role_by_id(self, role_id):
        roles = self.get_query("select id, name, permanent from roles where id=?", (role_id, ))
        if len(roles) > 0:
            role = self._role_object(roles[0])
            role.users = self.get_users_in_role(role.role_id)
            return role

        return None

    def get_role_by_name(self, role_name):
        roles = self.get_query("select id, name, permanent from roles where name like upper(?)", (role_name, ))
        if len(roles) > 0:
            role = self._role_object(roles[0])
            role.users = self.get_users_in_role(role.role_id)
            return role

        return None

    def role_exists(self, role_name):
        roles = self.get_query("select id, name, permanent from roles where name like upper(?)", (role_name, ))

        return len(roles) > 0

    def role_id_exists(self, role_id):
        roles = self.get_query("select id, name, permanent from roles where id=?", (role_id, ))

        return len(roles) > 0

    def is_user_part_of_role(self, user_id = 0, role_id = 0):
        data = self.get_query("select userid, roleid from user_roles where userid=? and roleid=?", (user_id, role_id))

        return len(data) > 0

    def add_user_to_role(self, user_id, role_id):
        self.set_query("insert into user_roles (userid, roleid) values (?, ?)", (user_id, role_id))

        return True

    def expire_user_by_id(self, user_id):
        self.set_query("delete from users where userid=?", (user_id, ))
        return True

    def delete_user_by_id(self, user_id):
        self.set_query("delete from users where userid=?", (user_id, ))
        self.set_query("delete from user_roles where userid=?", (user_id, ))

        return True

    def get_users_in_role(self, role_id):
        user_ids = self.get_query("select userid from user_roles where roleid=?", (role_id, ))

        users = []
        for userid in user_ids:
            user = self.get_user_by_id(userid)
            users.append(user)

        return users

    def get_roles_for_user(self, user_id):
        names = self.get_query("select name from roles where id in (select roleid from user_roles where userid=?)", (user_id, ))
        roles = []

        for name in names:
            roles.append(name[0])

        return roles

    def remove_user_from_role(self, user_id=0, role_id=0):
        self.set_query("delete from user_roles where userid=? and roleid=?", (user_id, role_id))

        return True

    def __del__(self):
        self.connection.close()

    def _user_object(self, user_tuple):
        u = User()
        u.user_id = int(user_tuple[0])
        u.username = user_tuple[1]
        u.name = user_tuple[2]
        u.created = user_tuple[3]

        return u

    def _role_object(self, role_tuple):
        r = Role()
        r.role_id = int(role_tuple[0])
        r.name = role_tuple[1]
        r.permanent = role_tuple[2]

        return r