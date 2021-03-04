## Requirements
- PostgreSQL
  - `docker run -d -p 5432:5432 -v $(pwd)/sql:/data -e POSTGRES_PASSWORD=password --name postgres-db postgres:9.3`
- RabbitMQ
  - `docker run -d -p 5672:5672 -e RABBITMQ_DEFAULT_VHOST=my_vhost rabbitmq:3.8`

## Setup
- Modify variables in `config.py` as required
- Run script:
```
python3 -m venv venv
source venv/bin/activate
pip install wheel
pip install -r requirements.txt
celery -A application worker -l INFO
```

## How to run
```
python app.py
```

## API
- Auth
    - `POST /api/signup` user signup
    - `POST /api/login` user login, returns `access_token`
    - `POST /api/logout` user logout
- Todo
    - `GET /api/todo` get all tasks
    - `GET /api/todo/<id:int>` returns task with id `:id`
    - `POST /api/todo` create new task
    - `PATCH /api/todo/<id:int>` edit task
    - `DELETE /api/todo/<id:int>` delete task
    - `POST /api/todo/<id:int>/execute` mark task as done

## Model examples
- Signup and login
```
{
    "email":"name@example.com",
    "password": "my_pass"
}
```
- Todo
```
{
    "title": "My great task",
    "end_date": "2022-04-05 23:59:59",
    "description": "Learn Flask"
}
```