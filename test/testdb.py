import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

from db.db import Database
from server_service import Service

class TestDatabase(unittest.TestCase):
    def test_test1(self):
        self.assertEqual(1, 1)

    def test_thetest(self):
        mydb = Database()
        arr = mydb.test()

        self.assertEqual(len(arr), 1)

    def test_role_exists(self):
        mydb = Database()
        self.assertFalse(mydb.role_exists("developer"))

    
    def test_create_and_delete_role(self):
        mydb = Database()
        created = mydb.create_role("testing")
        self.assertIsNotNone(created)
        self.assertEqual(created.name, "TESTING")

        deleted = mydb.delete_role("testing")
        self.assertTrue(deleted)

    def test_create_similar_name_roles(self):
        mydb = Database()
        created = mydb.create_role("developer1")
        self.assertIsNotNone(created)
        created = mydb.create_role("developer11")
        self.assertIsNotNone(created)
        created = mydb.create_role("developer2")
        self.assertIsNotNone(created)
        created = mydb.create_role("developer22")
        self.assertIsNotNone(created)

        deleted = mydb.delete_role("developer1")
        self.assertTrue(deleted)
        deleted = mydb.delete_role("developer11")
        self.assertTrue(deleted)
        deleted = mydb.delete_role("developer2")
        self.assertTrue(deleted)
        deleted = mydb.delete_role("developer22")
        self.assertTrue(deleted)

    def test_fail_to_delete_permanent_role(self):
        mydb = Database()
        role = mydb.get_role("developer")
        self.assertIsNotNone(role)
        deleted = mydb.delete_role("development")
        self.assertFalse(deleted)

    def test_user_belongs_to_role(self):
        mydb = Database()
        service = Service()
        user = service.get_user(1)
        role = mydb.get_role_by_name("developer")
        self.assertIsNotNone(user)
        self.assertIsNotNone(role)

        exists = mydb.is_user_part_of_role(userid = user.userid, roleid=role.roleid)
        self.assertTrue(exists)