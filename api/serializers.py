from rest_framework import serializers
from .models import Post, User


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username', read_only=True)
    created_date = serializers.DateTimeField(format="%Y %B %d")

    class Meta:
        model = Post
        fields = ['author', 'title', 'text', 'created_date']
        read_only_fields = ('likes', 'dislikes', )


class UserSerializer(serializers.ModelSerializer):
    last_activity = serializers.DateTimeField(format="%Y %B %d %H:%M:%S")
    last_login = serializers.DateTimeField(format="%Y %B %d %H:%M:%S")

    class Meta:
        model = User
        fields = ['last_activity', 'last_login']
