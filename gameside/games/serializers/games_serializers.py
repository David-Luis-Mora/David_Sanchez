from shared.serializers import BaseSerializer

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
            'released_at': instance.released_at,
            'pegi': instance.get_pegi_display(),
            'description': instance.description,
            # 'category': instance.category,
            # 'platforms': instance.platforms.all(),
        }   



class ReviewsSerializer(BaseSerializer):
    def __init__(self, to_serialize, *, fields=[], request=None):
        super().__init__(to_serialize, fields=fields, request=request)

    def serialize_instance(self, instance) -> dict:

        return {
            'id': instance.pk,
            'comment': instance.comment,
            'rating': instance.rating,
            #'game': instance.game,
            #'author': instance.author,
            'created_at': instance.created_at,
            'updated_at': instance.updated_at,
        }   