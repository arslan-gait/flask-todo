from flask import current_app as app

from application import db
from application.email import send_update_todo_status_email
from application.models import Todo
from application.error import TodoNotFoundError, InvalidParametersError


def get_todo_by_id(user, todo_id):
    return Todo.query.filter_by(id=todo_id, user_id=user.id).first()


def get_all_todos(user):
    return Todo.query.filter_by(user_id=user.id)


def edit_todo(user, request, todo_id):
    body = request.get_json()
    current_todo = get_todo_by_id(user, todo_id)
    if current_todo is None:
        raise TodoNotFoundError

    current_todo.update(body)
    try:
        db.session.commit()
    except Exception as e:
        app.logger.error(e)
        raise InvalidParametersError


def mark_todo(user, todo_id):
    current_todo = get_todo_by_id(user, todo_id)
    if current_todo is None:
        raise TodoNotFoundError
    if not current_todo.is_completed:
        current_todo.is_completed = True
        send_update_todo_status_email(current_todo)
        db.session.commit()


def delete_todo(user, todo_id):
    todo_entity = get_todo_by_id(user, todo_id)
    if todo_entity is None:
        raise TodoNotFoundError
    db.session.query(Todo).filter(Todo.id == todo_id).delete()
    db.session.commit()


def create_todo(request, user):
    body = request.get_json()
    todo = Todo(**body)
    todo.is_completed = False
    user.todos.append(todo)
    db.session.add(todo)
    db.session.commit()
