import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
import time
from db.db import Database
from server_service import Service

class TestService(unittest.TestCase):
    myservice = None
    def setUp(self):
        self.myservice = Service()

    def test_test1(self):
        self.assertEqual(1, 1)

    def test_create_role(self):
        role = self.myservice.new_role("12345")

        self.assertEqual(role.name, "12345")
        delete = self.myservice.delete_role_by_name("12345")
        self.assertTrue(delete)

    def test_add_user_to_role(self):
        user = self.myservice.get_user_by_id(1)
        role = self.myservice.new_role("roletotest")

        self.assertIsNotNone(user)
        self.assertTrue(user.user_id > 0)
        self.assertIsNotNone(role)
        self.assertTrue(role.role_id > 0)

        is_added = self.myservice.add_user_to_role(user.user_id, role.role_id)

        self.assertTrue(is_added)

        is_deleted = self.myservice.delete_role_by_name("roletotest")

        self.assertTrue(is_deleted)

    def test_users_in_roles(self):
        is_deleted = self.myservice.delete_role_by_name("testfortest")
        user1 = self.myservice.get_user_by_id(1)
        user2 = self.myservice.get_user_by_id(2)
        role = self.myservice.new_role("testfortest")

        self.assertIsNotNone(user1)
        self.assertIsNotNone(user2)
        self.assertIsNotNone(role)
        self.assertTrue(len(role.users) == 0)

        self.myservice.add_user_to_role(user_id = user1.user_id, role_id = role.role_id)
        self.myservice.add_user_to_role(user_id = user2.user_id, role_id = role.role_id)

        refreshed_role = self.myservice.get_role_by_id(role.role_id)
        self.assertEqual(len(refreshed_role.users), 2)

        is_deleted = self.myservice.delete_role_by_name("testfortest")
        self.assertTrue(is_deleted)

    def test_user_should_be_in_two_roles(self):
        user = self.myservice.get_user_by_id(1)
        self.myservice.delete_role_by_name("role1")
        self.myservice.delete_role_by_name("role2")

        role1 = self.myservice.new_role("role1")
        role2 = self.myservice.new_role("role2")

        self.myservice.add_user_to_role(user_id=user.user_id, role_id=role1.role_id)
        self.myservice.add_user_to_role(user_id=user.user_id, role_id=role2.role_id)

        refreshed_user = self.myservice.get_user_by_id(1)

        self.assertEqual(refreshed_user.roles, ["ROLE1", "ROLE2"])
        ok = self.myservice.delete_role_by_name("role1")
        self.assertTrue(ok)
        ok = self.myservice.delete_role_by_name("ROLE2")
        self.assertTrue(ok)

    def test_add_same_role_to_user(self):
        ok = self.myservice.delete_role_by_name("double_agent")
        role = self.myservice.new_role("double_agent")
        user = self.myservice.get_user_by_id(1)

        ok = self.myservice.add_user_to_role(user_id=user.user_id, role_id=role.role_id)
        self.assertTrue(ok)
        ok = self.myservice.add_user_to_role(user_id=user.user_id, role_id=role.role_id)
        self.assertTrue(ok)

        refreshed_user = self.myservice.get_user_by_id(1)
        self.assertEqual(refreshed_user.roles, ["DOUBLE_AGENT"])
        self.assertEqual(len(refreshed_user.roles), 1)

        ok = self.myservice.delete_role_by_name("double_agent")
        self.assertTrue(ok)

    def test_add_and_remove_user_from_role(self):
        role = self.myservice.delete_role_by_name("developer007")
        role = self.myservice.new_role("developer007")
        user = self.myservice.get_user_by_id(1)

        ok = self.myservice.add_user_to_role(user_id=user.user_id, role_id=role.role_id)
        self.assertTrue(ok)
        refreshed_role = self.myservice.get_role_by_name("developer007")
        self.assertEqual(len(refreshed_role.users), 1)
        ok = self.myservice.remove_user_from_role(user_id=user.user_id, role_id=role.role_id)
        refreshed_role1 = self.myservice.get_role_by_name("developer007")
        self.assertEqual(len(refreshed_role1.users), 0)

        ok = self.myservice.delete_role_by_name("developer007")
        self.assertTrue(ok)

    def test_delete_role_by_id(self):
        role = self.myservice.new_role("deletebyid")
        ok = self.myservice.delete_role_by_id(role.role_id)
        self.assertTrue(ok)

        role = self.myservice.get_role_by_name("deletebyid")
        self.assertIsNone(role)

    def test_expired(self):
        start = time.time()
        still_valid = start + 600
        expired_time = start - 600

        self.assertFalse(self.myservice.is_expired(still_valid))
        self.assertTrue(self.myservice.is_expired(expired_time))