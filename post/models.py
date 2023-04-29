from django.contrib.auth import get_user_model
from django.db import models


class Post(models.Model):
    text = models.TextField()
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

