from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import PostViewSet, PutDislike, PutLike, VotesAnalytic, PostCreateView, UserActivity


urlpatterns = [
    path('', PostViewSet.as_view({'get': 'list'}), name='posts'),
    path('login/', obtain_auth_token),
    path('post-create/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/', PostViewSet.as_view({'get': 'retrieve'}), name='post_detail'),
    path('post/<int:post_id>/like/', PutLike.as_view(), name='post_like'),
    path('post/<int:post_id>/dislike/', PutDislike.as_view(), name='post_dislike'),
    path('api/analytics/', VotesAnalytic.as_view(), name='like_count'),
    path('user/activity/', UserActivity.as_view(), name='user_activity'),

]
