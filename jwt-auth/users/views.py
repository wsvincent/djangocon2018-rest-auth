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