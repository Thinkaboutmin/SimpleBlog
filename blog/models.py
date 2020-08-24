from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    header = models.CharField(max_length=100, unique=True, primary_key=True)
    sub_header = models.CharField(max_length=200, null=True, blank=True)
    content = models.TextField()
    pub_date = models.DateTimeField(blank=True)
    revision_date = models.DateTimeField(null=True, blank=True)
    revision_author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="revision_author", blank=True)

    def __str__(self):
        return self.header


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    comment_date = models.DateTimeField(blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True)
    reply = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    content = models.CharField(max_length=5000)
