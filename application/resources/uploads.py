from flask import current_app
from flask_restful import reqparse, request, abort, Resource, fields, marshal_with
from application import db
from werkzeug.utils import secure_filename
from application.libs import gcv_label

import os
import base64

parser = reqparse.RequestParser()
parser.add_argument('file')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

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
        API_KEY = 'AIzaSyBHdeK5TxbfowdrbBYw-IclID0oIC5dHaA'
        DEST_LANG = 'ko'
        if 'file' not in request.files:
            return {'message': 'no file found'}

        file = request.files['file']
        if file:
            image_content = base64.b64encode(file.read())
            #filename = secure_filename(file.filename)
            #file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            #response_output = gcv_label.fetch_image_data(os.path.join(current_app.config['UPLOAD_FOLDER'], filename), print_output=False, dest_lang=DEST_LANG,
            #           api_key = API_KEY)
            response_output = gcv_label.fetch_image_data(image_content, print_output=False, dest_lang=DEST_LANG,
                       api_key = API_KEY)
            #$output = exec("python imageProcess.py photos/nixon-resignation-letter-1974.jpg -d ko -k AIzaSyBHdeK5TxbfowdrbBYw-IclID0oIC5dHaA 2>&1");
            return response_output, 201
