# theologos

### Create a Django Virtual Environment
Follow instructions at https://docs.djangoproject.com/en/4.1/intro/contributing/#getting-a-copy-of-django-s-development-version

### Activate Django Virtual Environment
```
source ~/.virtualenvs/djangodev/bin/activate
```

### Create and apply migrations
```
python manage.py makemigrations
python manage.py migrate
```

### Run Django development server
```
python manage.py runserver
```
Go to urls in `theologos/urls.py`.
