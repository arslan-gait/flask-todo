from celery import Celery
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

from config import Config
from application.error import MyException

db = SQLAlchemy()
jwt = JWTManager()
bcrypt = Bcrypt()


def handle_error(my_error):
    return my_error.serialize


def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)

    celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)

    db.init_app(app)
    jwt.init_app(app)
    app.register_error_handler(MyException, handle_error)

    with app.app_context():
        from application.routes import auth, todo

        db.create_all()

        app.register_blueprint(auth.bp)
        app.register_blueprint(todo.bp)

    return app
