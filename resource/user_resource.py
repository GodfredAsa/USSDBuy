from flask_jwt_extended import jwt_required
from flask_restful import Resource
from constants.user_constants import INVALID_PHONE_NUMBER, USER_ALREADY_EXISTS, ATTRIBUTE_ERROR, \
    USER_ADDING_FAILED, USER_NOT_FOUND, USER_DELETED_SUCCESS
from model.user_model import UserModel
from utils.helpers import is_valid_phone_number
from utils.user_data import user_data
import http.client as status
from utils.helpers import return_message


class AddUserResource(Resource):

    @jwt_required
    def post(self):
        data = user_data()
        try:
            if not is_valid_phone_number(data['phoneNumber']):
                return return_message(status.BAD_REQUEST, INVALID_PHONE_NUMBER), status.BAD_REQUEST
            if UserModel.find_user_by_number(data["phoneNumber"]):
                return return_message(status.BAD_REQUEST, USER_ALREADY_EXISTS.format(data["phoneNumber"])), \
                    status.BAD_REQUEST
            user = UserModel(data["phoneNumber"])
            user.save_user_to_db()
            return user.json(), status.CREATED
        except AttributeError as e:
            print(ATTRIBUTE_ERROR.format(e))
            return return_message(status.BAD_REQUEST, USER_ADDING_FAILED), status.BAD_REQUEST


class ListOfUsersResource(Resource):
    @jwt_required
    def get(self):
        return [user.json() for user in UserModel.find_all_users()]


class BlacklistUserResource(Resource):
    @jwt_required
    def put(self, phoneNumber: str):
        if not is_valid_phone_number(phoneNumber):
            return return_message(status.BAD_REQUEST, INVALID_PHONE_NUMBER), status.BAD_REQUEST
        user = UserModel.find_user_by_number(phoneNumber)
        if not user:
            return return_message(status=status.NOT_FOUND, message=USER_NOT_FOUND)
        user.is_whitelisted = False
        user.save_user_to_db()
        return user.json(), status.OK


class WhitelistUserResource(Resource):
    @jwt_required
    def put(self, phoneNumber: str):
        if not is_valid_phone_number(phoneNumber):
            return return_message(status.BAD_REQUEST, INVALID_PHONE_NUMBER), status.BAD_REQUEST
        user = UserModel.find_user_by_number(phoneNumber)
        if not user:
            return return_message(status=status.NOT_FOUND, message=USER_NOT_FOUND)
        user.is_whitelisted = True
        user.save_user_to_db()
        return user.json(), status.OK


class EditAndDeleteUserResource(Resource):
    @jwt_required
    def delete(self, phoneNumber):
        if not is_valid_phone_number(phoneNumber):
            return return_message(status.BAD_REQUEST, INVALID_PHONE_NUMBER), status.BAD_REQUEST
        user = UserModel.find_user_by_number(phoneNumber)
        if not user:
            return return_message(status=status.NOT_FOUND, message=USER_NOT_FOUND)
        user.delete_user_from_db()
        return return_message(status=status.OK, message=USER_DELETED_SUCCESS)

    @jwt_required
    def put(self, phoneNumber):
        data = user_data()
        user = UserModel.find_user_by_number(phoneNumber)
        try:
            if not user:
                return return_message(status.BAD_REQUEST, USER_NOT_FOUND), status.BAD_REQUEST
            if not is_valid_phone_number(data['phoneNumber']):
                return return_message(status.BAD_REQUEST, INVALID_PHONE_NUMBER), status.BAD_REQUEST
            if UserModel.find_user_by_number(data["phoneNumber"]):
                return return_message(status.CONFLICT, USER_ALREADY_EXISTS.format(data["phoneNumber"])), status.BAD_REQUEST
            user.phone_number = data["phoneNumber"]
            user.save_user_to_db()
            return user.json(), status.CREATED
        except AttributeError as e:
            print(ATTRIBUTE_ERROR.format(e))
            return return_message(status.BAD_REQUEST, "User Update Unsuccessful"), status.BAD_REQUEST





