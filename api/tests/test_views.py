import pytest
import ipdb
from django.utils import timezone
from django.urls import reverse
from api.models import Post, Like, DisLike


@pytest.mark.django_db
class TestPostViews:

    def test_create_post(self, api_client_authenticated, user):
        assert Post.objects.count() == 0
        path = reverse('post-create')
        request_data = {
            'title': 'test_title',
            'text': 'test_text',
            'author': user.id,
            'created_date': timezone.now()
        }
        response = api_client_authenticated.post(path, request_data)
        assert response.status_code == 201
        assert Post.objects.count() == 1

    def test_post_detail(self, api_client_authenticated, post):
        path = reverse('post_detail', kwargs={'pk': post.id})
        response = api_client_authenticated.get(path)

        assert response.status_code == 200

    def test_list_post(self, api_client_authenticated, post):
        path = reverse('posts')
        response = api_client_authenticated.get(path)

        assert response.status_code == 200
        assert Post.objects.count() == 1

    def test_post_like(self, api_client_authenticated, user, post):

        assert Like.objects.count() == 0

        path = reverse('post_like', kwargs={'post_id': post.id})
        response = api_client_authenticated.get(path)

        assert response.status_code == 200
        assert Like.objects.count() == 1

    def test_post_dislike(self, api_client_authenticated, user, post):

        assert DisLike.objects.count() == 0

        path = reverse('post_dislike', kwargs={'post_id': post.id})
        response = api_client_authenticated.get(path)

        assert response.status_code == 200
        assert DisLike.objects.count() == 1

    def test_like_count(self, api_client_authenticated, user, post):

        path = reverse('like_count')
        response = api_client_authenticated.get(path, {'date_from': '2021-09-08', 'date_to': '2021-09-11'})

        assert response.status_code == 200

    def test_user_activity(self, api_client_authenticated, user, post):
        path = reverse('user_activity')
        response = api_client_authenticated.get(path)

        assert response.status_code == 200
        assert response.json() == [
            {
                'last_activity': user.last_activity,
                'last_login': user.last_login,
            }
        ]
