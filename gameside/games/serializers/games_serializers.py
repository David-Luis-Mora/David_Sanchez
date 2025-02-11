from shared.serializers import BaseSerializer
from categories.serializers.categories_serializers import CategoriesSerializer
from platforms.serializers.platforms_serializers import PlatformSerializer
from users.serializers.users_serializers import UserSerializer

class GamesSerializer(BaseSerializer):
    def __init__(self, to_serialize, *, fields=[], request=None):
        super().__init__(to_serialize, fields=fields, request=request)

    def serialize_instance(self, instance) -> dict:

        return {
            'id': instance.pk,
            'title': instance.title,
            'slug': instance.slug,
            'cover': self.build_url(instance.cover.url),
            'price': float(instance.price),
            'stock': instance.stock,
            'released_at': instance.released_at.isoformat(),
            'pegi': instance.get_pegi_display(),
            'category': CategoriesSerializer(instance.category).serialize(),
            'description': instance.description,
            'platforms': PlatformSerializer(instance.platforms.all(),request=self.request).serialize() 
        }

    def serialize_queryset(self, queryset) -> list:
        return [self.serialize_instance(game) for game in queryset]



class ReviewsSerializer(BaseSerializer):
    def __init__(self, to_serialize, *, fields=[], request=None):
        super().__init__(to_serialize, fields=fields, request=request)

    def serialize_instance(self, instance) -> dict:

        return {
            'id': instance.pk,
            'comment': instance.comment,
            'rating': instance.rating,
            'game': GamesSerializer(instance.game,request=self.request).serialize(),
            'author': UserSerializer(instance.author).serialize(),
            'created_at': instance.created_at,
            'updated_at': instance.updated_at,  
        }