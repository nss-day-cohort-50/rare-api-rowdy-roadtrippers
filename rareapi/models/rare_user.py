from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE

class RareUser(models.Model):

    user = models.OneToOneField(User, on_delete=CASCADE)
    bio = models.CharField(max_length=50)
    profile_image_url = models.CharField(max_length=100)
    created_on = models.DateField
    active = models.BooleanField