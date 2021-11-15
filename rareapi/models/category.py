from django.db import models
from django.db.models.deletion import CASCADE

class Category(models.Model):

    label = models.CharField(max_length=50)
    