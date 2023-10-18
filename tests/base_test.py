import os
from unittest import TestCase
from app import app
from constants.app_constants import SQLALCHEMY_DATABASE_URI, DB_CONNECTION_STRING, PROPAGATE_EXCEPTIONS
from db import db


class BaseTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        app.config[SQLALCHEMY_DATABASE_URI] = os.environ.get(SQLALCHEMY_DATABASE_URI[11:], DB_CONNECTION_STRING[:-7])
        app.config['DEBUG'] = False
        app.config[PROPAGATE_EXCEPTIONS] = True

        with app.app_context():
            db.init_app(app)

    def setUp(self) -> None:
        app.config[SQLALCHEMY_DATABASE_URI] = os.environ.get(SQLALCHEMY_DATABASE_URI[11:], DB_CONNECTION_STRING[:-7])
        with app.app_context():
            db.create_all()
        self.app = app.test_client
        self.app_context = app.app_context

    def tearDown(self) -> None:
        with app.app_context():
            db.session.remove()
            db.drop_all()
