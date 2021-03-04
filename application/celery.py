from celery import Celery

from config import Config

app = Celery('application',
             broker=Config.CELERY_BROKER_URL,
             backend=Config.CELERY_RESULT_BACKEND,
             include=['application.tasks'])

app.conf.update(
    result_expires=3600,
)

if __name__ == '__main__':
    app.start()
