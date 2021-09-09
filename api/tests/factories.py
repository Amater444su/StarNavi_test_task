from django.contrib.auth import get_user_model
import factory
from factory.django import DjangoModelFactory
from api.models import Post, Like, DisLike

User = get_user_model()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"User{n}")
    email = factory.Sequence(lambda n: f"user{n}p@test.com")


class PostFactory(DjangoModelFactory):
    class Meta:
        model = Post

    author = factory.SubFactory(UserFactory)
    title = 'test_title'
    text = 'test_text'


class LikeFactory(DjangoModelFactory):
    class Meta:
        model = Like

    user = factory.SubFactory(UserFactory)
    post = factory.SubFactory(PostFactory)


class DislikeFactory(DjangoModelFactory):
    class Meta:
        model = DisLike

    user = factory.SubFactory(UserFactory)
    post = factory.SubFactory(PostFactory)