class Config:
    FLASK_ENV = 'development'
    SECRET_KEY = 'my_secret'
    APP_HOST = '0.0.0.0'
    APP_PORT = 5000
    APP_DEBUG = True
    LOGIN_TOKEN_HOURS = 1

    DB_NAME = "postgres"
    DB_HOST = "localhost"
    DB_PORT = "5432"
    DB_USER = "postgres"
    DB_PASSWORD = "password"
    SQLALCHEMY_DATABASE_URI = 'postgresql://{0}:{1}@{2}:{3}/{4}'.format(DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    CELERY_BROKER_URL = 'amqp://localhost:5672/my_vhost'
    CELERY_RESULT_BACKEND = 'rpc://'

    EMAIL_MOCK = True
    EMAIL_LOGIN = ''
    EMAIL_PASSWORD = ''
