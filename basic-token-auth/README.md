A working example of basic and token authentication with Django REST Framework. Step-by-step instructions available at `instructions.md`.

## Features

- Django 2.1 and Python 3.7
- custom user model
- sign up, log in, and log out
- users list/detail endpoints

## Quick Setup

```
$ git clone https://github.com/wsvincent/djangocon2018-rest-auth/tree/master/basic-token-auth
$ pipenv shell
(env) $ pipenv install
(env) $ python manage.py runserver
```

## Endpoints

- Log in: [http://127.0.0.1:8000/rest-auth/login/](http://127.0.0.1:8000/rest-auth/login/)
- Log out: [http://127.0.0.1:8000/rest-auth/logout/](http://127.0.0.1:8000/rest-auth/logout/)
- Sign up: [http://127.0.0.1:8000/rest-auth/registration/](http://127.0.0.1:8000/rest-auth/registration/)
- Users List: [http://127.0.0.1:8000/users/](http://127.0.0.1:8000/users/)
- Users Detail: [http://127.0.0.1:8000/users/1/](http://127.0.0.1:8000/users/1/)

## Switching to Token Authentication

To switch over there are three steps required:

1. Update `INSTALLED_APPS` by adding `'rest_framework.authtoken'`
2. Switch the `REST_FRAMEWORK` setting from `BasicAuthentication` to `TokenAuthentication`
3. Migrate the database to reflect the new changes

```python
# example_project/settings.py
INSTALLED_APPS = [
    # Local
    'users.apps.UsersConfig',

    # 3rd party
    'rest_framework',
    'rest_framework.authtoken', # new

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        # 'rest_framework.authentication.BasicAuthentication'
        'rest_framework.authentication.TokenAuthentication', # new
    ],
}
```

```
(env) $ python manage.py migrate
```

If you run the server again and look at the admin you'll see `Tokens` now.
