import ipdb
from django.db.models.functions import TruncDate
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, viewsets
from django.shortcuts import get_object_or_404
from api.serializers import PostSerializer, UserSerializer
from api.models import Post, Like, DisLike, User
from django.db.models import Q, Count
from datetime import datetime


class PostViewSet(viewsets.ViewSet):
    """List and Detail display for post"""
    permission_classes = [AllowAny]

    def list(self, request):
        """List display for all Posts"""
        queryset = Post.objects.all()
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Display a single post"""
        queryset = Post.objects.all()
        post = get_object_or_404(queryset, pk=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)


class PostCreateView(generics.CreateAPIView):
    """Create post and assign posts author"""
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PutLike(APIView):
    """Put like to the post"""
    def get(self, request, post_id):
        user = self.request.user
        post = Post.objects.filter(id=post_id).first()
        if user in post.likes.all():
            return Response()
        elif user in post.dislikes.all():
            post.dislikes.remove(user)
            DisLike.objects.filter(id=post_id).first().delete()

        post.likes.add(user)
        Like.objects.create(post_id=post_id, user=user)
        return Response()


class PutDislike(APIView):
    """Put dislike to the post"""
    def get(self, request, post_id):
        user = self.request.user
        post = Post.objects.filter(id=post_id).first()
        if user in post.dislikes.all():
            return Response()
        elif user in post.likes.all():
            post.likes.remove(user)
            Like.objects.filter(id=post_id).first().delete()

        post.dislikes.add(user)
        DisLike.objects.create(post_id=post_id, user=user)
        return Response()


class VotesAnalytic(APIView):
    """Displays all likes and dislikes statistic
        for the particular date"""
    def get(self, request):
        date_from = self.request.query_params['date_from']
        date_to = self.request.query_params['date_to']
        date_from = datetime.strptime(date_from, '%Y-%m-%d')
        date_to = datetime.strptime(date_to, '%Y-%m-%d')
        total_likes = Like.objects.filter(Q(like_date__gte=date_from) & Q(like_date__lte=date_to)) \
            .values(date=TruncDate('like_date')).annotate(likes=Count('id'))
        total_dislikes = DisLike.objects.filter(Q(dislike_date__gte=date_from) & Q(dislike_date__lte=date_to)) \
            .values(date=TruncDate('dislike_date')).annotate(dislikes=Count('id'))

        return Response(f'total likes {total_likes}, total dislikes {total_dislikes}')


class UserActivity(generics.ListAPIView):
    """Display last login and last activity for current user"""
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = User.objects.filter(id=self.request.user.id)
        return queryset
