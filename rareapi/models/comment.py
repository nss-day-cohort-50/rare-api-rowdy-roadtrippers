from django.db import models
from django.db.models.deletion import CASCADE


class Comment(models.Model):

    post = models.ForeignKey("Post", on_delete=CASCADE,
                             related_name='comments')
    author = models.ForeignKey("RareUser", on_delete=CASCADE)
    content = models.CharField(max_length=500)
    created_on = models.DateField()
