import logging.config

from flask import Flask, Blueprint
import settings
from api.todo.endpoints import Todo, TodoList
from api.user.endpoints import User, UserList
from api.upload.endpoints import UploadList
from api.restful import api
from database import db

app = Flask(__name__)
#logging.config.fileConfig('logging.conf')
log = logging.getLogger(__name__)


def configure_app(flask_app):
    #flask_app.config['SERVER_NAME'] = settings.FLASK_SERVER_NAME
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.SQLALCHEMY_TRACK_MODIFICATIONS
    flask_app.config['UPLOAD_FOLDER'] = settings.UPLOAD_FOLDER
    flask_app.config['ALLOWED_EXTENSIONS'] = settings.ALLOWED_EXTENSIONS


def initialize_app(flask_app):
    configure_app(flask_app)
    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)
    ## register all app URLs
    api.add_resource(TodoList, '/todos')
    api.add_resource(Todo, '/todos/<todo_id>')
    api.add_resource(UserList, '/users')
    api.add_resource(User, '/users/<user_id>')
    api.add_resource(UploadList, '/upload')
    flask_app.register_blueprint(blueprint)

    db.app = flask_app
    db.init_app(flask_app)
    #db.drop_all()
    db.create_all()

def main():
    initialize_app(app)
    log.info('>>>>> Starting development server at http://{}/api/ <<<<<'.format(app.config['SERVER_NAME']))
    app.run(debug=settings.FLASK_DEBUG)

if __name__ == "__main__":
    main()