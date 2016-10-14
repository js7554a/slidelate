import logging.config
import settings

from flask import Flask, Blueprint
from flask_restful import Api
from api.todo.endpoints import Todo, TodoList
from api.user.endpoints import User, UserList
from api.upload.endpoints import UploadList
from database import db

app = Flask(__name__)

log = logging.getLogger(__name__)
logging.config.fileConfig('logging.conf')
log = logging.getLogger(__name__)

app.config['SERVER_NAME'] = settings.FLASK_SERVER_NAME
app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.SQLALCHEMY_TRACK_MODIFICATIONS
app.config['UPLOAD_FOLDER'] = settings.UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = settings.ALLOWED_EXTENSIONS

blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(blueprint)
api.add_resource(TodoList, '/todos')    
api.add_resource(Todo, '/todos/<todo_id>')
api.add_resource(UserList, '/users')
api.add_resource(User, '/users/<user_id>')
api.add_resource(UploadList, '/upload')
app.register_blueprint(blueprint)

db.app = app
db.init_app(app)
db.drop_all()
db.create_all()

def main():
    log.info('>>>>> Starting development server at http://{}/api/ <<<<<'.format(app.config['SERVER_NAME']))
    app.run(debug=settings.FLASK_DEBUG)

if __name__ == "__main__":
    main()