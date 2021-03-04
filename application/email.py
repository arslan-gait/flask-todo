from application.tasks import send_async_email


def send_update_todo_status_email(todo):
    send_async_email.delay({
        'to': todo.user.email,
        'subject': 'Task "{}"'.format(todo.title),
        'contents': 'Task status with title "{}" changed'.format(todo.title)
    })
