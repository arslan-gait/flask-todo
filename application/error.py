from flask import jsonify


class MyException(Exception):
    def __init__(self):
        Exception.__init__(self)

    @property
    def serialize(self):
        dictionary = {'msg': self.message}
        serialized = jsonify(dictionary)
        serialized.status_code = self.status_code
        return serialized


class InvalidParametersError(MyException):
    def __init__(self):
        MyException.__init__(self)
        self.message = 'Bad parameters error'
        self.status_code = 400


class UnauthorizedError(MyException):
    def __init__(self):
        MyException.__init__(self)
        self.message = 'Unauthorized'
        self.status_code = 401


class UserExistsError(MyException):
    def __init__(self):
        MyException.__init__(self)
        self.message = 'User exists'
        self.status_code = 400


class TodoNotFoundError(MyException):
    def __init__(self):
        MyException.__init__(self)
        self.message = 'Todo not found'
        self.status_code = 404


class BlacklistedTokenError(MyException):
    def __init__(self):
        MyException.__init__(self)
        self.message = 'Token is blacklisted. Login again.'
        self.status_code = 401


class AlreadyLoggedOutError(MyException):
    def __init__(self):
        MyException.__init__(self)
        self.message = 'You were already logged out'
        self.status_code = 400
