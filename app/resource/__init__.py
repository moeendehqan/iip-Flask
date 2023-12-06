from flask_restful import Api
from .login import Login
from .cookie import Cookie

api = Api()

api.add_resource(Login, '/login')
api.add_resource(Cookie, '/cookie')
