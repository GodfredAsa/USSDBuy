from model.user_model import UserModel
from tests.unit.unit_base_test import UnitBaseTest


class UserTest(UnitBaseTest):
    def test_create_user(self) -> None:
        user = UserModel("0549977883")
        self.assertEqual(user.phone_number, "0549977883")
        self.assertTrue(user.is_whitelisted)
        self.assertEqual(user.id, None)

    def test_user_json(self):
        """ since the userId is dynamically generated I need to wrote it """
        user = UserModel("0549977883")
        expected = {
            'status_code': 1,
            'message': 'active',
            'phoneNumber': "0549977883"
        }
        user.user_id = "1234"
        actual = user.json()
        self.assertDictEqual(actual, expected)
