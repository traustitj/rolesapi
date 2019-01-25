from db.db import Database
import json
import requests
from flask import request
from flask import Response
from models import User


class Service:
    mydb = None

    def __init__(self):
        self.mydb = Database()
        
    def index(self):
        arr = self.mydb.get_roles()
        return json.dumps(arr)

    def get_user_by_id(self, userid):
        user = self.mydb.get_user_by_id(userid)
        if not user is None:
            return user
        
        returned = requests.get('http://tempo-test.herokuapp.com/7d1d085e-dbee-4483-aa29-ca033ccae1e4/1/user/%s/' % (userid))
        user = json.loads(returned.text)
        user = self.mydb.save_user(user)
        return user

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