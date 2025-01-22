import uuid

from django.conf import settings
from django.db import models


# Create your models here.
class Order(models.Model):
    class Statu(models.IntegerChoices):
        INITIATED = 0
        CONFIRMED = 1
        CANCELLED = 2
        PAID = 3

    status = models.SmallIntegerField(
        choices=Statu,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    key = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders'
    )
    games = models.ManyToManyField('games.Game', related_name='orders')
