from rest_framework import serializers

from post.models import Post
from user.serializers import UserSerializer


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'author', 'text')


class PostListSerializer(serializers.ModelSerializer):
    author = UserSerializer()

    class Meta:
        model = Post
        fields = ('id', 'author', 'text')


class PostCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('id', 'text', 'author')
        read_only_fields = ('author', )
