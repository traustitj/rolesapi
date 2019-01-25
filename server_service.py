from db.db import Database
import json
import requests
from flask import request
from flask import Response
from models import User
import time


class Service:
    mydb = None
    expire = 5 * 60

    def __init__(self):
        self.mydb = Database()
        
    def index(self):
        arr = self.mydb.get_roles()
        return json.dumps(arr)

    def get_user_by_id(self, user_id):
        user = self.mydb.get_user_by_id(user_id)
        if not user is None:
            if self.is_expired(user.created + self.expire) == True:
                self.expire_user_by_id(1)
            else:
                return user
        
        resp = requests.get('http://tempo-test.herokuapp.com/7d1d085e-dbee-4483-aa29-ca033ccae1e4/1/user/%s/' % (user_id))
        if resp.status_code == 200:
            user = json.loads(resp.text)
            user = self.mydb.save_user(user)
            return user
        else:
            self.delete_user(user_id)
            return None

    def is_expired(self, time_to_check):
        right_now = time.time()
        return (right_now > time_to_check)

    def expire_user_by_id(self, user_id):
        self.mydb.expire_user_by_id(user_id)
        return True

    def delete_user(self, user_id):
        self.mydb.delete_user_by_id(user_id)
        return True

    def get_role_by_id(self, role_id):
        return self.mydb.get_role_by_id(role_id)

    def get_role_by_name(self, name):
        return self.mydb.get_role_by_name(name)

    def new_role(self, role_name):
        return self.mydb.create_role(role_name)

    def delete_role_by_name(self, role_name):
        return self.mydb.delete_role_by_name(role_name)

    def delete_role_by_id(self, role_id):
        return self.mydb.delete_role_by_id(role_id)

    def add_user_to_role(self, user_id=0, role_id=0):
        user = self.mydb.get_user_by_id(user_id)
        role = self.mydb.get_role_by_id(role_id)

        if user == None or role == None:
            return False

        if self.user_part_of_role(user_id=user.user_id, role_id=role.role_id):
            return True

        user = self.get_user_by_id(user_id)
        role = self.get_role_by_id(role_id)

        if user == None or role == None:
            return False

        return self.mydb.add_user_to_role(user_id, role_id)

    def remove_user_from_role(self, user_id=0, role_id=0):
        return self.mydb.remove_user_from_role(user_id=user_id, role_id=role_id)

    def user_part_of_role(self, user_id=0, role_id=0):
        return self.mydb.is_user_part_of_role(user_id=user_id, role_id=role_id)