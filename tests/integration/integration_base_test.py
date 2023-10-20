import os
from unittest import TestCase
from app import app
from constants.app_constants import SQLALCHEMY_DATABASE_URI, DB_CONNECTION_STRING
from db import db


class IntegrationBaseTest(TestCase):
    def setUp(self) -> None:
        app.config[SQLALCHEMY_DATABASE_URI] = os.environ.get(SQLALCHEMY_DATABASE_URI[11:], DB_CONNECTION_STRING[:-7])

        with app.app_context():
            db.init_app(app)
            db.create_all()
        self.app = app.test_client()
        self.app_context = app.app_context

    def tearDown(self) -> None:
        # ensure the DB is blanked and dropped
        with app.app_context():
            db.session.remove()
            db.drop_all()
