from model.admin_model import AdminModel
from tests.unit.unit_base_test import UnitBaseTest


class UserTest(UnitBaseTest):
    admin = AdminModel("test@test.io", "1234")

    def test_create_admin(self):
        admin = UserTest.admin
        self.assertTrue(admin.is_admin)
        self.assertEqual(admin.password, "1234")
        self.assertEqual(admin.email, "test@test.io")

    def test_json(self):
        admin = UserTest.admin
        admin.admin_id = "1234"
        expected_json = {
            "adminId": "1234",
            "email": "test@test.io"
        }

        self.assertDictEqual(expected_json, admin.json())



