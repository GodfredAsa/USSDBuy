from flask_restful import reqparse
from constants.user_constants import BLANK_ERROR


_user_parser = reqparse.RequestParser()
_user_parser.add_argument("phoneNumber", type=str, required=True, help=BLANK_ERROR.format("phoneNumber"))


def user_data():
    return _user_parser.parse_args()
