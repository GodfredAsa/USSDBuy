import json
from typing import Dict, Any, Tuple

from constants.uri import ADMIN_LOGIN_URI, ADMIN_SIGNUP_URI, ADD_USER_URI, LIST_OF_USERS_URI, EDIT_DELETE_USER_URI
from tests.base_test import SystemBaseTest
from tests.system.data import ADMIN_DATA, HEADERS, USER_DATA, USERS_DATA


class UserTest(SystemBaseTest):
    def setUp(self) -> Dict[str, Any]:
        super(UserTest, self).setUp()
        with self.app() as client:
            with self.app_context():
                client.post(ADMIN_SIGNUP_URI, data=ADMIN_DATA)
                admin_login_response = client.post(ADMIN_LOGIN_URI, data=json.dumps(ADMIN_DATA), headers=HEADERS)
                token = json.loads(admin_login_response.data)['token']
                return {"token": token}

    def test_add_user_no_auth(self):
        with self.app() as client:
            with self.app_context():
                response = client.post(ADD_USER_URI, data=USER_DATA, headers=HEADERS)
                self.assertDictEqual(json.loads(response.data), {'msg': 'Missing Authorization Header'})

    def test_add_user_no_phone_number(self):
        with self.app() as client:
            with self.app_context():
                token = self.setUp()['token']
                AUTH_HEADER = {"Authorization": "Bearer {}".format(token)}
                response = client.post(ADD_USER_URI, data={"phoneNumber": None}, headers=AUTH_HEADER)
                expected_dict = {"message": {"phoneNumber": "phoneNumber Cannot Be Blank."}}
                self.assertDictEqual(json.loads(response.data), expected_dict)

    def test_add_user_invalid_number(self):
        with self.app() as client:
            with self.app_context():
                USER_DATA["phoneNumber"] = "024567"
                token = self.setUp()['token']
                AUTH_HEADER = {"Authorization": "Bearer {}".format(token)}
                response = client.post(ADD_USER_URI, data=USER_DATA, headers=AUTH_HEADER)
                expected_dict = {'status': 400, 'message': 'Invalid Phone Number'}
                self.assertDictEqual(json.loads(response.data), expected_dict)

    def test_add_user(self):
        with self.app() as client:
            with self.app_context():
                token = self.setUp()['token']
                AUTH_HEADER = {"Authorization": "Bearer {}".format(token)}
                response = client.post(ADD_USER_URI, data=USER_DATA, headers=AUTH_HEADER)
                expected_dict = {'status_code': 1, 'message': 'active', 'phoneNumber': '0543334447'}
                self.assertDictEqual(json.loads(response.data), expected_dict)

    def test_get_users(self):
        with self.app() as client:
            with self.app_context():
                token = self.setUp()['token']
                AUTH_HEADER = {"Authorization": "Bearer {}".format(token)}

                # adding users
                for i in range(len(USERS_DATA)):
                    client.post(ADD_USER_URI, data=USERS_DATA[i], headers=AUTH_HEADER)

                response = client.get(LIST_OF_USERS_URI, data=USERS_DATA[i], headers=AUTH_HEADER)

                expected = [
                    {"status_code": 1, "message": "active", "phoneNumber": "0543334447"},
                    {"status_code": 1, "message": "active", "phoneNumber": "0543334448"},
                    {"status_code": 1, "message": "active", "phoneNumber": "0543334449"}
                ]

                self.assertEqual(len(json.loads(response.data)), 3, "Assert there are 3 users registered")

                for j in range(len(json.loads(response.data))):
                    self.assertDictEqual(json.loads(response.data)[j], expected[j])

    def test_update_added_user(self):
        with self.app() as client:
            with self.app_context():
                token = self.setUp()['token']
                AUTH_HEADER = {"Authorization": "Bearer {}".format(token)}
                # add users
                for i in range(len(USERS_DATA)):
                    client.post(ADD_USER_URI, data=USERS_DATA[i], headers=AUTH_HEADER)

                uri = f"/api/v1/users/{'0543334440'}"
                response = client.put(uri, data={"phoneNumber": "0543334442"}, headers=AUTH_HEADER)
                self.assertDictEqual(json.loads(response.data), {"status": 400, "message": "User Not Found"})

#                 update with already taken number
                uri = f"/api/v1/users/{'0543334447'}"
                response = client.put(uri, data={"phoneNumber": "0543334448"}, headers=AUTH_HEADER)
                expected = {"status": 409, "message": "A User With 0543334448 Already Exists."}
                self.assertDictEqual(json.loads(response.data), expected)

#               update existing number with non-existing new number
                response = client.put(uri, data={"phoneNumber": "0543334453"}, headers=AUTH_HEADER)
                expected = {"status_code": 1, "message": "active", "phoneNumber": "0543334453"}
                self.assertDictEqual(json.loads(response.data), expected)


class BlacklistAndWhitelistUserTest(SystemBaseTest):
    def setUp(self) -> Dict[str, Any]:
        super(BlacklistAndWhitelistUserTest, self).setUp()
        with self.app() as client:
            with self.app_context():
                client.post(ADMIN_SIGNUP_URI, data=ADMIN_DATA)
                admin_login_response = client.post(ADMIN_LOGIN_URI, data=json.dumps(ADMIN_DATA), headers=HEADERS)
                token = json.loads(admin_login_response.data)['token']
                return {"token": token}

    def test_blacklist_and_whitelist_user(self):
        with self.app() as client:
            with self.app_context():
                token = self.setUp()['token']
                AUTH_HEADER = {"Authorization": "Bearer {}".format(token)}

                # adding user 0543334447
                response = client.post(ADD_USER_URI, data=USER_DATA, headers=AUTH_HEADER)
                expected = {"status_code": 1, "message": "active", "phoneNumber": "0543334447"}
                self.assertDictEqual(json.loads(response.data), expected)

                # blacklist user
                response = client.put("/api/v1/users/0543334447/blacklist", data=USER_DATA, headers=AUTH_HEADER)
                expected = {"status_code": 1, "message": "blocked", "phoneNumber": "0543334447"}
                self.assertDictEqual(json.loads(response.data), expected)

                # whitelisting a user
                response = client.put("/api/v1/users/0543334447/whitelist", data=USER_DATA, headers=AUTH_HEADER)
                expected = {"status_code": 1, "message": "active", "phoneNumber": "0543334447"}
                self.assertDictEqual(json.loads(response.data), expected)


class DeletingUserTest(SystemBaseTest):
    def setUp(self) -> Dict[str, Any]:
        super(DeletingUserTest, self).setUp()
        with self.app() as client:
            with self.app_context():
                client.post(ADMIN_SIGNUP_URI, data=ADMIN_DATA)
                admin_login_response = client.post(ADMIN_LOGIN_URI, data=json.dumps(ADMIN_DATA), headers=HEADERS)
                token = json.loads(admin_login_response.data)['token']
                return {"token": token}

    def test_deleting_existing_user(self):
        with self.app() as client:
            with self.app_context():
                token = self.setUp()['token']
                AUTH_HEADER = {"Authorization": "Bearer {}".format(token)}

                # adding user 0543334447
                client.post(ADD_USER_URI, data=USER_DATA, headers=AUTH_HEADER)

                # delete you with wrong number
                response = client.delete(f"/api/v1/users/{'0543334440'}", headers=AUTH_HEADER)
                self.assertDictEqual(json.loads(response.data), {"status": 404, "message": "User Not Found"})

                # deleting user with user number
                response = client.delete(f"/api/v1/users/{'0543334447'}", headers=AUTH_HEADER)
                expected = {"status": 200, "message": "User Deleted Successfully."}
                self.assertDictEqual(json.loads(response.data),  expected)
























