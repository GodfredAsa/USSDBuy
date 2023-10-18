import bcrypt
from flask import request
from flask_restful import Resource
from constants.user_constants import USER_ALREADY_EXISTS, INVALID_EMAIL, ATTRIBUTE_ERROR, \
    INVALID_CREDENTIALS, ADMIN_NOT_ADDED
from model.admin_model import AdminModel
from utils.admin_data import admin_data
from utils.helpers import return_message, is_valid_email, verify_credentials, generate_token
import http.client as status


class AddAdminResource(Resource):
    def post(self):
        data = admin_data()
        try:
            if AdminModel.admin_exist(data['email']):
                return return_message(status.BAD_REQUEST, USER_ALREADY_EXISTS.format(data['email'])), status.BAD_REQUEST
            admin = AdminModel(**data)
            if not is_valid_email(admin.email):
                return return_message(status.BAD_REQUEST, INVALID_EMAIL), status.BAD_REQUEST
            admin.password = bcrypt.hashpw(admin.password.encode("utf-8"), bcrypt.gensalt())
            admin.save_to_db()
            return admin.json(), status.CREATED
        except AttributeError as e:
            print(ATTRIBUTE_ERROR.format(e))
            return return_message(status.BAD_REQUEST, ADMIN_NOT_ADDED), status.BAD_REQUEST


class AdminLoginResource(Resource):

    def post(self):
        data = request.get_json()
        if not verify_credentials(data['email'], data['password']):
            return return_message(status.BAD_REQUEST, INVALID_CREDENTIALS), status.BAD_REQUEST
        user = AdminModel.find_by_email(data["email"])
        return {
            "token": generate_token(user),
            'user': user.json()
        }, status.OK
