# Step by Step Instructions

How to create this project from scratch yourself!

## Install Django

```
$ pipenv install django
$ pipenv shell
(env) $ django-admin startproject example_project .
```

## Create Custom User Model

(env) $ python manage.py startapp users

````
```python
# example_project/settings.py
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
````

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
(env) $ python manage.py runserver
```

Log in to admin and confirm you can view/edit Users app

[http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin).

## Install Django REST Framework

```
(env) $ pipenv install djangorestframework
```

```python
# example_project/settings.py
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

Explicitly add the default Authentication Class setting.

```python
# example_project/settings.py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication'
    ],
}
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
# example_project/urls.py
from django.contrib import admin
from django.urls import path, include # new

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')), # new
]
```

```
(env) $ python manage.py runserver
```

Users list endpoints: [http://127.0.0.1:8000/users/](http://127.0.0.1:8000/users/)

Users detail endpoints: [http://127.0.0.1:8000/users/1/](http://127.0.0.1:8000/users/1/)

## Log In and Log Out Endpoints

```
(env) $ pipenv install django-rest-auth
```

```python
# example_project/settings.py
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
# example_project/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('rest-auth/', include('rest_auth.urls')), # new
]
```

http://127.0.0.1:8000/rest-auth/login/

http://127.0.0.1:8000/rest-auth/logout/

## User Registration

```
(env) $ pipenv install django-allauth
```

```python
# example_project/settings.py
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
# example_project/urls.py
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
