import unittest
import sys
import os
import time
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

from db.db import Database
from server_service import Service

class TestDatabase(unittest.TestCase):
    mydb = None

    def setUp(self):
        self.mydb = Database()

    def test_test1(self):
        self.assertEqual(1, 1)

    def test_get_user(self):
        user = self.mydb.get_user_by_id(1)

        self.assertIsNotNone(user)
        self.assertEqual(user.user_id, 1)

    def test_role_exists(self):
        self.assertTrue(self.mydb.role_exists("developer"))
    
    def test_create_and_delete_role(self):
        created = self.mydb.create_role("testing")
        self.assertIsNotNone(created)
        self.assertEqual(created.name, "TESTING")

        deleted = self.mydb.delete_role_by_name("testing")
        self.assertTrue(deleted)

    def test_create_similar_name_roles(self):
        created = self.mydb.create_role("developer1")
        self.assertIsNotNone(created)
        created = self.mydb.create_role("developer11")
        self.assertIsNotNone(created)
        created = self.mydb.create_role("developer2")
        self.assertIsNotNone(created)
        created = self.mydb.create_role("developer22")
        self.assertIsNotNone(created)

        deleted = self.mydb.delete_role_by_name("developer1")
        self.assertTrue(deleted)
        deleted = self.mydb.delete_role_by_name("developer11")
        self.assertTrue(deleted)
        deleted = self.mydb.delete_role_by_name("developer2")
        self.assertTrue(deleted)
        deleted = self.mydb.delete_role_by_name("developer22")
        self.assertTrue(deleted)

    def test_fail_to_delete_permanent_role(self):
        role = self.mydb.get_role_by_name("developer")
        self.assertIsNotNone(role)
        deleted = self.mydb.delete_role_by_name("development")
        self.assertFalse(deleted)

    def test_user_belongs_to_role(self):
        user = self.mydb.get_user_by_id(1)
        role = self.mydb.get_role_by_name("developer")
        self.assertIsNotNone(user)
        self.assertIsNotNone(role)

        exists = self.mydb.is_user_part_of_role(user_id = user.user_id, role_id=role.role_id)
        self.assertFalse(exists)
