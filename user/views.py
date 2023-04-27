from rest_framework import generics

from user.serializers import UserSerializer


class UserRegistryView(generics.CreateAPIView):
    serializer_class = UserSerializer
