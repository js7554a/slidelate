from flask_restful import reqparse, abort, Resource, fields, marshal_with
from database import db
from database.models import User as u
from flask import jsonify

user_fields = {
    'username': fields.String,
    'password_hash' : fields.String
}

TODOS = {
    'todo1': {'task': 'build an API'},
    'todo2': {'task': '?????'},
    'todo3': {'task': 'profit!'},
}


def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in TODOS:
        abort(404, message="Todo {} doesn't exist".format(todo_id))

parser = reqparse.RequestParser()
parser.add_argument('username')
parser.add_argument('password')

# Todo
# shows a single todo item and lets you delete a todo item
class User(Resource):
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
class UserList(Resource):
    @marshal_with(user_fields)
    def get(self):
        users = u.query.all()
        return users,201

    def post(self):
        args = parser.parse_args()
        #return args, 201
        username = args['username']
        password = args['password']

        if username is None or password is None:
            abort(400)
        if u.query.filter_by(username = username).first() is not None:
            abort(400)

        user = u(username = username, password_hash = None)
        user.hash_password(password)
        db.session.add(user)
        db.session.commit()
        return {'username': user.username}, 201
