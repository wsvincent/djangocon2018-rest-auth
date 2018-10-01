# Step by Step Instructions

How to create this project from scratch yourself!

## Install Django & Create Custom User Model

```
$ pipenv install django
$ pipenv shell
(env) $ django-admin startproject jwtauth_project .
(env) $ python manage.py startapp users
```

```python
# jwtauth_project/settings.py
INSTALLED_APPS = [
    # Local
    'users.apps.UsersConfig', # new

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

AUTH_USER_MODEL = 'users.CustomUser' # new
```

```python
# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    pass
```

```python
# users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser


admin.site.register(CustomUser, CustomUserAdmin)
```

```
(env) $ python manage.py makemigrations users
(env) $ python manage.py migrate
(env) $ python manage.py createsuperuser
```

## Install Django REST Framework

```
(env) $ pipenv install djangorestframework
```

```python
# jwtauth_project/settings.py
INSTALLED_APPS = [
    # Local
    'users.apps.UsersConfig',

    # 3rd party
    'rest_framework', # new

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```

```
(env) $ python manage.py migrate
```

## Users Endpoints

Create Users list and detail endpoints.

```
(env) $ touch users/serializers.py
(env) $ touch users/urls.py
```

```python
# users/serializers.py
from django.contrib.auth import get_user_model
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('id', 'username',)
```

```python
# users/views.py
from django.contrib.auth import get_user_model
from rest_framework import generics

from .serializers import UserSerializer

CustomUser = get_user_model()

class UserList(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
```

```python
# users/urls.py
from django.urls import path

from .views import UserList, UserDetail

urlpatterns = [
    path('', UserList.as_view()),
    path('<int:pk>/', UserDetail.as_view()),
]
```

```python
# socialauth_project/urls.py
from django.contrib import admin
from django.urls import path, include # new

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')), # new
]
```

```
(env) $ python manage.py migrate
(env) $ python manage.py runserver
```

Users list endpoints: [http://127.0.0.1:8000/users/](http://127.0.0.1:8000/users/)

Users detail endpoints: [http://127.0.0.1:8000/users/1/](http://127.0.0.1:8000/users/1/)

## Log In and Log Out Endpoints

```
(env) $ pipenv install django-rest-auth
```

```python
# jwtauth_project/settings.py
INSTALLED_APPS = [
    # Local
    'users.apps.UsersConfig',

    # 3rd party
    'rest_framework',
    'rest_auth', # new

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```

```python
# jwtauth_project/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('rest-auth/', include('rest_auth.urls')), # new
]
```

```
(env) $ python manage.py runserver
```

http://127.0.0.1:8000/rest-auth/login/

http://127.0.0.1:8000/rest-auth/logout/

## User Registration

```
(env) $ pipenv install django-allauth
```

```python
# socialauth_project/settings.py
INSTALLED_APPS = [
    # Local
    'users.apps.UsersConfig',

    # 3rd party
    'rest_framework',
    'rest_auth',
    'django.contrib.sites', # new
    'allauth', # new
    'allauth.account', # new
    'rest_auth.registration', # new
]

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' # new

SITE_ID = 1 # new
```

```python
# jwtauth_project/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')), # new
]
```

```
(env) $ python manage.py migrate
(env) $ python manage.py runserver
```

http://127.0.0.1:8000/rest-auth/registration/

## JWTs

```
(env) $ pipenv install djangorestframework-jwt
```

Require auth for API endpoints and add `JSONWebTokenAuthentication`.

```python
# jwtauth_project/settings.py
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
}
```

```python
# jwtauth_project/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token # new

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('api-token-auth/', obtain_jwt_token), # new
]
```

## Test Endpoint

Assumes username of `admin` and password of `testpass123`. Use your own superuser account info here.

```
$ curl -X POST -d "username=admin&password=testpass123" http://localhost:8000/api-token-auth/{"token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6IndzdiIsImV4cCI6MTUzODE1MjE2NiwiZW1haWwiOiJ3aWxsQHdzdmluY2VudC5jb20ifQ.vNVOKWzkbq--YMqRv0W5Zyf5JZ_4NP_bYxEgnDPqnJU"}%
```

API endpoints require authentication now:

```
$ curl -X POST -d "username=admin&password=testpass123" http://localhost:8000/users/
```

Output will be:

```
{"detail":"Authentication credentials were not provided."}%
```

To access protected API URLs you must include the `Authorization: JWT <your_token>` in the HTTP header.

```
$ curl -H "Authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6IndzdiIsImV4cCI6MTUzODE1MjE2NiwiZW1haWwiOiJ3aWxsQHdzdmluY2VudC5jb20ifQ.vNVOKWzkbq--YMqRv0W5Zyf5JZ_4NP_bYxEgnDPqnJU" http://localhost:8000/users/
```

Output will be:

```
[{"id":1,"username":"admin"}]%
```

**Note**: Default is for tokens to expire after 5 minutes. Might get a `Signature has expired` error if wait longer than that. Log in again to generate a refreshed token. Or update `JWT_EXPIRATION_DELTA` under settings as specified [in the docs](http://getblimp.github.io/django-rest-framework-jwt/).
