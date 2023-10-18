import uuid

from db import db
# from utils.helpers import generate_uuid


class AdminModel(db.Model):
    __tablename__ = "admins"
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.String(20))
    is_admin = db.Column(db.Boolean, default=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

    def __init__(self, email, password):
        self.admin_id = str(uuid.uuid4())
        self.email = email
        self.is_admin = True
        self.password = password

    def json(self):
        return {
            "adminId": self.admin_id,
            "email": self.email
        }

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_email(cls, email: str) -> 'AdminModel':
        return AdminModel.query.filter_by(email=email).first()

    @classmethod
    def find_id(cls, admin_id: str) -> 'AdminModel':
        return AdminModel.query.filter_by(admin_id=admin_id).first()

    @classmethod
    def admin_exist(cls, email):
        if not AdminModel.find_by_email(email):
            return False
        else:
            return True
