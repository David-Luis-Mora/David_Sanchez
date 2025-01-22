import uuid

from django.conf import settings
from django.db import models

# Create your models here.


class Token(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='token', on_delete=models.CASCADE
    )
    key = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
