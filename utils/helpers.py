import uuid
import re

import bcrypt
from flask_jwt_extended import create_access_token
from model.admin_model import AdminModel


def generate_uuid():
    return str(uuid.uuid4())


def return_message(status: int, message: str):
    return {'status': status, 'message': message}


def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None


def is_valid_phone_number(phone_number):
    pattern = r'0[2-9][0-9]{8}'
    return re.match(pattern, phone_number) is not None


def generate_token(admin: 'AdminModel') -> str:
    return create_access_token(admin.email)


def whitelisted_active_blacklisted_block(status: bool) -> str:
    return "active" if status else "blocked"



def verify_credentials(email, password):
    if not AdminModel.find_by_email(email):
        return False
    hashed_password = AdminModel.find_by_email(email).password
    if bcrypt.hashpw(password.encode('utf-8'), hashed_password) == hashed_password:
        return True
    else:
        return False
