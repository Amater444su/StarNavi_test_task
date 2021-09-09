from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True)
    last_activity = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.username


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_author')
    title = models.CharField(max_length=150)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='post_like')
    dislikes = models.ManyToManyField(User, related_name='post_dislike')

    def __str__(self):
        return self.title


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='like_user')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='like_post')
    like_date = models.DateTimeField(auto_now_add=True)


class DisLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dislike_user')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='dislike_user')
    dislike_date = models.DateTimeField(auto_now_add=True)
