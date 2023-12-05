from flask_restful import Api
from .hello_world import HelloWorld
from .login import Login

api = Api()

api.add_resource(HelloWorld, '/helloworld')
api.add_resource(Login, '/login')
