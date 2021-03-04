from datetime import datetime

from flask_bcrypt import generate_password_hash, check_password_hash
from sqlalchemy import Column, Integer

from application import db
from application.email import send_update_todo_status_email


class BlacklistToken(db.Model):
    __tablename__ = 'blacklist_tokens'

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.now()

    @staticmethod
    def check_blacklist(auth_token):
        res = BlacklistToken.query.filter_by(token=str(auth_token)).first()
        if res:
            return True
        else:
            return False


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    hashed_password = db.Column(db.String(100))

    todos = db.relationship(
        'Todo', backref=db.backref('user.id', lazy=True))

    def hash_password(self, password):
        self.hashed_password = generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)


class Todo(db.Model):
    __tablename__ = 'todo'
    id = Column(Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.Text)
    end_date = db.Column(db.DateTime)
    is_completed = db.Column(db.Boolean, default=False)

    user = db.relationship('User', backref='todo.id')
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete='cascade'))

    def update(self, new_data):
        for key in new_data:
            if hasattr(self, key) and key != 'id':
                if key == 'is_completed' and self.is_completed != new_data[key]:
                    send_update_todo_status_email(self)
                setattr(self, key, new_data[key])
