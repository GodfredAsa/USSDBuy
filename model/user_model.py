from db import db
from utils.helpers import generate_uuid


class UserModel(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(20))
    phone_number = db.Column(db.String(10), nullable=False)
    is_whitelisted = db.Column(db.Boolean, default=True)

    def __init__(self, phone):
        self.user_id = generate_uuid()
        self.phone_number = phone
        self.is_whitelisted = True

    def __str__(self):
        return f"<User: ID:{self.id}, Phone number:{self.phone_number}, isWhitelisted:{self.is_whitelisted}>"

    def json(self):
        return {
            "userId": self.user_id,
            "phoneNumber": self.phone_number,
            "isWhitelisted": self.is_whitelisted
        }

    @classmethod
    def find_user_by_number(cls, phone_number: str) -> 'UserModel':
        return UserModel.query.filter_by(phone_number=phone_number).first()

    @classmethod
    def find_user_by_id(cls, _id: int) -> 'UserModel':
        return UserModel.query.filter_by(id=_id).first()

    @classmethod
    def find_user_by_uuid(cls, userId: str) -> 'UserModel':
        return UserModel.query.filter_by(user_id=userId).first()

    @classmethod
    def find_all_users(cls):
        return UserModel.query.all()

    def save_user_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_user_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

