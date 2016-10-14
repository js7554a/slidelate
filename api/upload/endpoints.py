from flask_restful import reqparse, request, abort, Resource, fields, marshal_with
from database import db
from werkzeug.utils import secure_filename
import os

parser = reqparse.RequestParser()
parser.add_argument('file')

# Todo
# shows a single todo item and lets you delete a todo item
class Upload(Resource):
    def get(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        return TODOS[todo_id]

    def delete(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        del TODOS[todo_id]
        return '', 204

    def put(self, todo_id):
        args = parser.parse_args()
        task = {'task': args['task']}
        TODOS[todo_id] = task
        return task, 201


# TodoList
# shows a list of all todos, and lets you POST to add new tasks
class UploadList(Resource):
    """
    @marshal_with(user_fields)
    def get(self):
        users = u.query.all()
        return users,201
    """

    def post(self):
        if 'file' not in request.files:
            return {'message': 'no file found'}

        file = request.files['file']

        if file:
            filename = secure_filename(file.filename)
            #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return {'filename' : filename}, 201
