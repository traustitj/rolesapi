from db.db import Database
import json
import requests
from flask import request
from flask import Response
from models import User


class Service:

    def index(self):
        mydb = Database()
        arr = mydb.test()
        return json.dumps(arr)

    def get_user(self, userid):
        mydb = Database()
        user = mydb.get_user(userid)
        if not user is None:
            ret = json.dumps("")
            return "From database %s - %s - %d - %d\n" % (user.username, user.name, user.user_id, user.created)
        
        returned = requests.get('http://tempo-test.herokuapp.com/7d1d085e-dbee-4483-aa29-ca033ccae1e4/1/user/%s/' % (userid))
        user = json.loads(returned.text)
        user = mydb.save_user(user)
        return "returned from web: %s - %s - %d - %d\n" % (user.username, user.name, user.user_id, user.created)

    def new_role(self, role_name):
        pass