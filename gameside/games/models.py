from django.conf import settings
from django.db import models

# from django.conf import settings


# Create your models here.
class Game(models.Model):
    class Pegi(models.IntegerChoices):
        PEGI3 = 3
        PEGI7 = 7
        PEGI12 = 12
        PEGI16 = 16
        PEGI18 = 18

    title = models.CharField(max_length=255, unique=True)
    slug = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    cover = models.ImageField(blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    stock = models.PositiveSmallIntegerField()
    released_at = models.DateField()
    pegi = models.IntegerField(
        choices=Pegi,
    )

    category = models.ForeignKey(
        'categories.Category',
        related_name='games',
        on_delete=models.CASCADE,
        blank=True,
    )
    platforms = models.ManyToManyField(
        'platforms.Platform',
        related_name='games',
    )


class Review(models.Model):
    comment = models.TextField()
    rating = models.SmallIntegerField()
    game = models.ForeignKey('games.Game', related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews'
    )
