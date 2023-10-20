from model.user_model import UserModel
from tests.integration.integration_base_test import IntegrationBaseTest


class UserTest(IntegrationBaseTest):
    def test_crud_user(self):
        with self.app_context():
            user = UserModel("02456563344")
            self.assertIsNone(user.find_user_by_number("02456563344"))

            # save and find user with number
            user.save_user_to_db()
            # number of users
            self.assertEqual(len(user.find_all_users()), 1)
            # user exists
            self.assertIsNotNone(user.find_user_by_number("02456563344"))

            # update number and assert previous and updated number
            user.phone_number = "0246666667"
            user.save_user_to_db()

            self.assertIsNone(user.find_user_by_number("02456563344"))
            self.assertIsNotNone(user.find_user_by_number("0246666667"))

            # delete and assert user
            user.delete_user_from_db()
            self.assertIsNone(user.find_user_by_number("02456563344"))








