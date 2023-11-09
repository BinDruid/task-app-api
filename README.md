# Simple To-Do application web api

Minimal django application to handle registering tasks with different tags.
The application has boiler plate code for celery tasks with a flower dashboard.

## Run Project

Build and run the containers:

```sh
$ docker-compose up --build
```

Open your browser to http://localhost:9000 to view the available endpoints or to http://localhost:5555 to view the Flower dashboard.

Run test:

```sh
$ docker compose exec django-api python manage.py test
```
