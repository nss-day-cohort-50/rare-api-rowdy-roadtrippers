from django.db import models
from django.db.models.deletion import CASCADE

class Post(models.Model):

    rare_user = models.ForeignKey("RareUser", on_delete=CASCADE)
    category = models.ForeignKey("Category", on_delete=CASCADE)
    title = models.CharField(max_length=50)
    publication_date = models.DateField()
    image_url = models.CharField(max_length=100)
    content = models.CharField(max_length=100)
    approved = models.BooleanField()
    post_tag = models.ManyToManyField("Tag", through="PostTag", related_name="tag")
    
