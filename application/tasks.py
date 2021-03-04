import yagmail

from config import Config
from .celery import app


@app.task
def send_async_email(message):
    if Config.EMAIL_MOCK:
        return f"Mocked email sent to {message['to']}"

    try:
        yag = yagmail.SMTP(user=Config.EMAIL_LOGIN, password=Config.EMAIL_PASSWORD)
        yag.send(to=message['to'], subject=message['subject'], contents=message['contents'])
        return f"Email sent successfully to {message['to']}"
    except Exception as e:
        return f"Error, email to {message['to']} was not sent: {e}"
