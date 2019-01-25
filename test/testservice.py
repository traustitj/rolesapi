import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

from db.db import Database
from server_service import Service

class TestService(unittest.TestCase):
    def test_test1(self):
        self.assertEqual(1, 1)

    def test_create_role(self):
        service = Service()
        role = service.new_role("12345")

        self.assertEqual(role.name, "12345")
        delete = service.delete_role_by_name("12345")
        self.assertTrue(delete)

    def test_add_user_to_role(self):
        service = Service()
        user = service.get_user_by_id(1)
        role = service.new_role("roletotest")

        self.assertIsNotNone(user)
        self.assertTrue(user.user_id > 0)
        self.assertIsNotNone(role)
        self.assertTrue(role.role_id > 0)

        is_added = service.add_user_to_role(user.user_id, role.role_id)

        self.assertTrue(is_added)

        is_deleted = service.delete_role_by_name("roletotest")

        self.assertTrue(is_deleted)

    def test_users_in_roles(self):
        service = Service()
        is_deleted = service.delete_role_by_name("testfortest")
        user1 = service.get_user_by_id(1)
        user2 = service.get_user_by_id(2)
        role = service.new_role("testfortest")

        self.assertIsNotNone(user1)
        self.assertIsNotNone(user2)
        self.assertIsNotNone(role)
        self.assertTrue(len(role.users) == 0)

        service.add_user_to_role(user_id = user1.user_id, role_id = role.role_id)
        service.add_user_to_role(user_id = user2.user_id, role_id = role.role_id)

        refreshed_role = service.get_role_by_id(role.role_id)
        self.assertEqual(len(refreshed_role.users), 2)

        is_deleted = service.delete_role_by_name("testfortest")
        self.assertTrue(is_deleted)

    def test_user_should_be_in_two_roles(self):
        service = Service()
        user = service.get_user_by_id(1)
        service.delete_role_by_name("role1")
        service.delete_role_by_name("role2")

        role1 = service.new_role("role1")
        role2 = service.new_role("role2")

        service.add_user_to_role(user_id=user.user_id, role_id=role1.role_id)
        service.add_user_to_role(user_id=user.user_id, role_id=role2.role_id)

        refreshed_user = service.get_user_by_id(1)

        self.assertEqual(refreshed_user.roles, ["ROLE1", "ROLE2"])
        ok = service.delete_role_by_name("role1")
        self.assertTrue(ok)
        ok = service.delete_role_by_name("ROLE2")
        self.assertTrue(ok)

    def test_add_same_role_to_user(self):
        service = Service()
        ok = service.delete_role_by_name("double_agent")
        role = service.new_role("double_agent")
        user = service.get_user_by_id(1)

        ok = service.add_user_to_role(user_id=user.user_id, role_id=role.role_id)
        self.assertTrue(ok)
        ok = service.add_user_to_role(user_id=user.user_id, role_id=role.role_id)
        self.assertTrue(ok)

        refreshed_user = service.get_user_by_id(1)
        self.assertEqual(refreshed_user.roles, ["DOUBLE_AGENT"])
        self.assertEqual(len(refreshed_user.roles), 1)

        ok = service.delete_role_by_name("double_agent")
        self.assertTrue(ok)

    def test_add_and_remove_user_from_role(self):
        service = Service()
        role = service.delete_role_by_name("developer007")
        role = service.new_role("developer007")
        user = service.get_user_by_id(1)

        ok = service.add_user_to_role(user_id=user.user_id, role_id=role.role_id)
        self.assertTrue(ok)
        refreshed_role = service.get_role_by_name("developer007")
        self.assertEqual(len(refreshed_role.users), 1)
        ok = service.remove_user_from_role(user_id=user.user_id, role_id=role.role_id)
        refreshed_role1 = service.get_role_by_name("developer007")
        self.assertEqual(len(refreshed_role1.users), 0)

        ok = service.delete_role_by_name("developer007")
        self.assertTrue(ok)

