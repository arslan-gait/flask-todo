from functools import wraps

from flask import request

from application.error import BlacklistedTokenError
from application.models import BlacklistToken


def check_blacklist_token(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        auth_token = auth_header.split(" ")[1] if auth_header else ''
        is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
        if is_blacklisted_token:
            raise BlacklistedTokenError
        return f(*args, **kwargs)

    return decorated_function
