from flask import Flask
from flask_cors import CORS
from app.resource import api
from app.models.Users import Users
def create_app():
    app = Flask(__name__)
    CORS(app)
    api.init_app(app)
    UsersModel = Users()
    UsersModel.create_super_user()
    return app
