from django.db import models
from users.models import User

# Create your models here.


class Tag(models.Model):
    tag_name = models.CharField(max_length=50)
    tag_type = models.CharField(max_length=50)
    tag_description = models.TextField()

    def __str__(self):
        return self.tag_name


class Question(models.Model):
    title = models.CharField(max_length=150)
    body = models.TextField(null=False, blank=False)
    owner = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name='questions')
    tags = models.ManyToManyField(Tag)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Solution(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name='solutions'
    )
    solution = models.TextField(null=False, blank=False)
    up_votes = models.IntegerField(default=0, editable=False)
    down_votes = models.IntegerField(default=0, editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.solution


class Comment(models.Model):
    solution = models.ForeignKey(
        Solution, on_delete=models.CASCADE, related_name='comments')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')

    def __str__(self):
        return self.comment


class Vote(models.Model):
    solution = models.ForeignKey(
        Solution, on_delete=models.CASCADE, related_name='votes')
    vote = models.BooleanField(null=True)
    owner = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name='votes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.owner} {self.vote}'


class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.DO_NOTHING)
