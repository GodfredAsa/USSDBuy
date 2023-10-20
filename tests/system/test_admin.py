from constants.uri import ADMIN_SIGNUP_URI, ADMIN_LOGIN_URI
from constants.user_constants import INVALID_EMAIL
from tests.base_test import SystemBaseTest
from tests.system.data import ADMIN_DATA, HEADERS
import json
import http.client as status
from utils.helpers import return_message


class AdminTestSystem(SystemBaseTest):
    def test_signup_admin_invalid_email(self):
        with self.app() as client:
            with self.app_context():
                ADMIN_DATA["email"] = "test_.com"
                response = client.post(ADMIN_SIGNUP_URI, data=ADMIN_DATA)
                self.assertEqual(response.status_code, status.BAD_REQUEST)
                response_dict = json.loads(response.data)
                self.assertDictEqual(return_message(status.BAD_REQUEST, INVALID_EMAIL), response_dict)

    def test_admin_signup_and_login(self):
        with self.app() as client:
            with self.app_context():
                # SIGN UP
                response = client.post(ADMIN_SIGNUP_URI, data=ADMIN_DATA)
                self.assertEqual(response.status_code, status.CREATED)

                # LOGIN AND OBTAIN TOKEN
                admin_login_response = client.post(ADMIN_LOGIN_URI, data=json.dumps(ADMIN_DATA), headers=HEADERS)
                token = json.loads(admin_login_response.data)['token']
                self.assertIsNotNone(token)

    def test_admin_signup_and_login_wrong_password(self):
        with self.app() as client:
            with self.app_context():
                # SIGN UP
                response = client.post(ADMIN_SIGNUP_URI, data=ADMIN_DATA)
                self.assertEqual(response.status_code, status.CREATED)

                # LOGIN WITH INVALID PASSWORD
                ADMIN_DATA["password"] = "pass"
                admin_login_response = client.post(ADMIN_LOGIN_URI, data=json.dumps(ADMIN_DATA), headers=HEADERS)
                expected_dict = {'status': 400, 'message': 'Invalid User Credentials'}
                self.assertDictEqual(json.loads(admin_login_response.data), expected_dict)

    def test_signup_admin_duplicate_email(self):
        with self.app() as client:
            with self.app_context():
                # first signup
                response = client.post(ADMIN_SIGNUP_URI, data=ADMIN_DATA)
                self.assertEqual(response.status_code, status.CREATED)
                response_dict = json.loads(response.data)

                self.assertIsNotNone(response_dict["adminId"])
                self.assertEqual(response_dict["email"], 'admin@test.io')

                # second signup with same email
                response_two = client.post(ADMIN_SIGNUP_URI, data=ADMIN_DATA)

                expected_dict = {"status": 400, "message": "A User With admin@test.io Already Exists."}
                self.assertDictEqual(json.loads(response_two.data), expected_dict)


class AdminRegistrationTestSystem(SystemBaseTest):
    def test_signup_admin_valid_email(self):
        with self.app() as client:
            with self.app_context():
                response = client.post(ADMIN_SIGNUP_URI, data=ADMIN_DATA)
                self.assertEqual(response.status_code, status.CREATED)
                response_dict = json.loads(response.data)
                response_dict["adminId"] = "123"
                self.assertDictEqual(response_dict, {'adminId': '123', 'email': 'admin@test.io'})

