from tests.unit.unit_base_test import UnitBaseTest
from utils.helpers import generate_uuid, return_message, is_valid_email, is_valid_phone_number, \
    whitelisted_active_blacklisted_block


class UtilsTest(UnitBaseTest):
    @staticmethod
    def test_generate_uuid() -> None:
        assert generate_uuid() is not None
        assert len(generate_uuid()) == 36

    @staticmethod
    def test_return_message() -> None:
        expected_message = {"status": 200, "message": "my test message"}
        assert expected_message == return_message(200, "my test message")

    def test_is_valid_email(self):
        self.assertEqual(is_valid_email("admin@admin.com"), True)
        self.assertEqual(is_valid_email("adminadmin.com"), False)
        self.assertEqual(is_valid_email("admina_dmin.com"), False)
        self.assertEqual(is_valid_email("@adminadmin.com"), False)
        self.assertEqual(is_valid_email("adminadmin@.com"), False)
        self.assertEqual(is_valid_email(""), False)

    def test_is_valid_number(self):
        self.assertTrue(is_valid_phone_number("0548889932"))
        self.assertFalse(is_valid_phone_number(""))
        self.assertFalse(is_valid_phone_number("054888993"))
        self.assertFalse(is_valid_phone_number("0548889"))

    def test_whitelisted_active_blacklisted_block(self):
        self.assertEqual(whitelisted_active_blacklisted_block(True), "active")
        self.assertEqual(whitelisted_active_blacklisted_block(False), "blocked")




