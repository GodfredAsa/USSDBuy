from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from constants.app_constants import SQLALCHEMY_DATABASE_URI, DB_CONNECTION_STRING, SQL_MODIFICATION_STRING, \
    PROPAGATE_EXCEPTIONS, JWT_KEY, JWT_SECRET
from constants.uri import ADMIN_SIGNUP_URI, ADMIN_LOGIN_URI, ADD_USER_URI
from db import db
from resource.admin_resource import AddAdminResource, AdminLoginResource
from resource.user_resource import AddUserResource

app = Flask(__name__)
jwt = JWTManager(app)
api = Api(app)

app.config[SQLALCHEMY_DATABASE_URI] = DB_CONNECTION_STRING
app.config[SQL_MODIFICATION_STRING] = False
app.config[PROPAGATE_EXCEPTIONS] = True
app.config[JWT_SECRET] = JWT_KEY


@app.before_first_request
def create_tables():
    db.create_all()


# API RESOURCE
# ADMIN
api.add_resource(AddAdminResource, ADMIN_SIGNUP_URI)
api.add_resource(AdminLoginResource, ADMIN_LOGIN_URI)

# USER API
api.add_resource(AddUserResource, ADD_USER_URI)


if __name__ == "__main__":
    db.init_app(app)
    app.run(port=5003, debug=True)
