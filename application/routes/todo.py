from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required

from application.decorators import check_blacklist_token
from application.util.auth_utils import get_user_from_jwt_identity
from application.schemas import todo_schema, short_todo_schema, validate_with_schema
from application.util.todo_utils import create_todo, get_all_todos, get_todo_by_id, edit_todo, delete_todo, \
    mark_todo

bp = Blueprint('todo', __name__)


@bp.route('/api/todo', methods=['POST', 'GET'])
@jwt_required()
@check_blacklist_token
def todo_by_body():
    user = get_user_from_jwt_identity()
    if request.method == 'GET':
        todos = get_all_todos(user)
        return jsonify(short_todo_schema.dump(todos, many=True))

    validate_with_schema(request, todo_schema)
    create_todo(request, user)
    return jsonify({'message': 'ok'})


@bp.route('/api/todo/<int:todo_id>', methods=['GET', 'PATCH', 'DELETE'])
@jwt_required()
@check_blacklist_token
def todo_by_id(todo_id):
    user = get_user_from_jwt_identity()
    if request.method == 'GET':
        todo_entity = get_todo_by_id(user, todo_id)
        return jsonify(todo_schema.dump(todo_entity))
    elif request.method == 'PATCH':
        edit_todo(user, request, todo_id)
    else:
        delete_todo(user, todo_id)

    return jsonify(status='ok')


@bp.route('/api/todo/<int:todo_id>/execute', methods=['POST'])
@jwt_required()
@check_blacklist_token
def execute_todo(todo_id):
    user = get_user_from_jwt_identity()
    mark_todo(user, todo_id)

    return jsonify(status='ok')
