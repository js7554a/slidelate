#need to run SET GOOGLE_APPLICATION_CREDENTIALS=C:\Users\Jake\projects\slidelate\credentials.json
import os

from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_httpauth import HTTPBasicAuth

db = SQLAlchemy()
api = Api()
auth = HTTPBasicAuth()

def create_app(environment=None):
	app = Flask(__name__)
	api_bp = Blueprint('api.v1', __name__, url_prefix='/api')
	api.init_app(api_bp)
	if not environment:
		environment = 'production' if os.environ.get('IS_HEROKU', None) else 'development'
	app.config.from_object('config.{}'.format(environment.capitalize()))

	db.init_app(app)
	import authentification
	from .resources.todos import Todo, TodoList
	from .resources.users import UserList, UserLogin
	from .resources.uploads import UploadList
	api.add_resource(TodoList, '/todos')
	api.add_resource(Todo, '/todos/<todo_id>')
	api.add_resource(UserList, '/users')
	api.add_resource(UserLogin, '/token')
	api.add_resource(UploadList, '/uploads')
	app.register_blueprint(api_bp)

	return app