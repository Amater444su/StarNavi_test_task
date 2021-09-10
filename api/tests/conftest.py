import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient
from api.tests.factories import UserFactory, PostFactory, LikeFactory, DislikeFactory

register(UserFactory)
register(PostFactory)
register(LikeFactory)
register(DislikeFactory)


@pytest.fixture
def user():
    return UserFactory()


@pytest.fixture
def api_client_authenticated(db, user):
    api_client = APIClient()
    api_client.force_authenticate(user=user)
    yield api_client
    api_client.force_authenticate(user=None)
