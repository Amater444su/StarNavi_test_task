from rest_framework import serializers
from api.models import Post, User

DATETIME_FORMAT = "%Y %B %d %H:%M:%S"


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username', read_only=True)
    created_date = serializers.DateTimeField(format=DATETIME_FORMAT)

    class Meta:
        model = Post
        fields = ['author', 'title', 'text', 'created_date']
        read_only_fields = ('likes', 'dislikes', )


class UserSerializer(serializers.ModelSerializer):
    last_activity = serializers.DateTimeField(format=DATETIME_FORMAT)
    last_login = serializers.DateTimeField(format=DATETIME_FORMAT)

    class Meta:
        model = User
        fields = ['last_activity', 'last_login']
