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
            'category': {
                'id': instance.category.pk,
                'name': instance.category.name,
                'slug': instance.category.slug,
                'description': instance.category.description,
                'color': instance.category.color,
            },
            'description': instance.description,
             'platforms': [
                {
                    'id': platform.pk,
                    'name': platform.name,
                    'slug': platform.slug,
                    'description': platform.description,
                    'logo': self.build_url(platform.logo.url),
                }
                for platform in instance.platforms.all()
            ],

        }   



class ReviewsSerializer(BaseSerializer):
    def __init__(self, to_serialize, *, fields=[], request=None):
        super().__init__(to_serialize, fields=fields, request=request)

    def serialize_instance(self, instance) -> dict:

        return {
            'id': instance.pk,
            'comment': instance.comment,
            'rating': instance.rating,
            'game': {
                'id': instance.game.pk,
                'title': instance.game.title,
                'slug': instance.game.slug,
                'description': instance.game.description,
                'cover': self.build_url(instance.game.cover.url),

                'price': instance.game.price,
                'stock': instance.game.stock,
                'released_at': instance.game.released_at,
                'pegi': instance.game.get_pegi_display(),
                'category': {
                    'id': instance.game.category.pk,
                    'name': instance.game.category.name,
                    'slug': instance.game.category.slug,
                    'description': instance.game.category.description,
                    'color': instance.game.category.color,
                },
                'platforms':[
                    {
                        'id': instance.platform.pk,
                        'name': instance.platform.name,
                        'slug': instance.platform.slug,
                        'description': instance.platform.description,
                        'logo': self.build_url(instance.platform.logo.url),
                    }
                    for platform in instance.game.platforms.all()
                ] 

            },
            'author':{
                'id': instance.author.id,
                'username': instance.author.username,
                'email': instance.author.email,
                'first_name': instance.author.first_name,
                'last_name': instance.author.last_name
            },
            'created_at': instance.created_at,
            'updated_at': instance.updated_at,
           
        }