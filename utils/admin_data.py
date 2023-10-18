
from flask_restful import reqparse
from constants.user_constants import BLANK_ERROR

_admin_parser = reqparse.RequestParser()
_admin_parser.add_argument("email", type=str, required=True, help=BLANK_ERROR.format("email"))
_admin_parser.add_argument("password", type=str, required=True, help=BLANK_ERROR.format("password"))


def admin_data():
    return _admin_parser.parse_args()




