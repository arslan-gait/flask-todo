from datetime import timedelta

from flask import current_app as app
from flask_jwt_extended import get_jwt_identity, create_access_token
from sqlalchemy.exc import IntegrityError

from application import db
from application.models import User, BlacklistToken
from application.error import UnauthorizedError, UserExistsError, AlreadyLoggedOutError
from application.schemas import user_schema, validate_with_schema


def handle_signup(request):
    body = request.get_json()
    password = body.pop('password')
    user = User(**body)
    user.hash_password(password)

    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError:
        raise UserExistsError


def handle_login(request):
    validate_with_schema(request, user_schema)
    email = request.json.get('email')
    password = request.json.get('password')

    user = get_user_from_email(email)
    if user is None or not user.check_password(password):
        raise UnauthorizedError

    access_token = get_access_token(email, app.config['LOGIN_TOKEN_HOURS'])
    response = {
        'access_token': access_token,
        'user': user_schema.dump(user)
    }
    return response


def handle_logout(request):
    auth_header = request.headers.get('Authorization')
    auth_token = auth_header.split(" ")[1] if auth_header else ''

    if auth_token:
        blacklist_token = BlacklistToken(token=auth_token)
        db.session.add(blacklist_token)
        try:
            db.session.commit()
        except IntegrityError:
            raise AlreadyLoggedOutError


def get_user_from_jwt_identity():
    email = get_jwt_identity()
    if email is None:
        raise UnauthorizedError
    return get_user_from_email(email)


def get_access_token(email, hours):
    return create_access_token(identity=email, expires_delta=timedelta(hours=hours))


def get_user_from_email(email):
    return User.query.filter_by(email=email).first()
