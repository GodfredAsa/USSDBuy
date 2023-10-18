from datetime import timedelta

from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from constants.app_constants import SQLALCHEMY_DATABASE_URI, DB_CONNECTION_STRING, SQL_MODIFICATION_STRING, \
    PROPAGATE_EXCEPTIONS, JWT_KEY, JWT_SECRET, JWT_ACCESS_TOKEN_EXPIRES
from constants.uri import ADMIN_SIGNUP_URI, ADMIN_LOGIN_URI, ADD_USER_URI, LIST_OF_USERS_URI, BLACKLIST_USER_URI, \
    WHITELIST_USER_URI, EDIT_DELETE_USER_URI
from db import db
from resource.admin_resource import AddAdminResource, AdminLoginResource
from resource.user_resource import AddUserResource, ListOfUsersResource, BlacklistUserResource, WhitelistUserResource, \
    EditAndDeleteUserResource

app = Flask(__name__)
jwt = JWTManager(app)
api = Api(app)

app.config[SQLALCHEMY_DATABASE_URI] = DB_CONNECTION_STRING
app.config[SQL_MODIFICATION_STRING] = False
app.config[PROPAGATE_EXCEPTIONS] = True
app.config[JWT_SECRET] = JWT_KEY
app.config[JWT_ACCESS_TOKEN_EXPIRES] = timedelta(hours=1)


@app.before_first_request
def create_tables():
    db.create_all()


# API RESOURCE
# ADMIN
api.add_resource(AddAdminResource, ADMIN_SIGNUP_URI)
api.add_resource(AdminLoginResource, ADMIN_LOGIN_URI)

# USER API
api.add_resource(AddUserResource, ADD_USER_URI)
api.add_resource(ListOfUsersResource, LIST_OF_USERS_URI)


api.add_resource(BlacklistUserResource, BLACKLIST_USER_URI)
api.add_resource(WhitelistUserResource, WHITELIST_USER_URI)

api.add_resource(EditAndDeleteUserResource, EDIT_DELETE_USER_URI)





# 0548670632

if __name__ == "__main__":
    db.init_app(app)
    app.run(port=5003, debug=True)
