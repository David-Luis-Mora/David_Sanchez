from django.db import models

class Platform(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField()
    logo = models.ImageField(blank=True, null=True, default='logos/default.jpg')
