from django.db import models
from django.db.models.deletion import CASCADE

class PostTag(models.Model):
    tag_id = models.ForeignKey('Tag', on_delete=CASCADE)
    post_id = models.ForeignKey('Post', on_delete=CASCADE)
