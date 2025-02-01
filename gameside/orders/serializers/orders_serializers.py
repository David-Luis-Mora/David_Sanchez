from shared.serializers import BaseSerializer


class OrdersSerializer(BaseSerializer):
    def __init__(self, to_serialize, *, fields=[], request=None):
        super().__init__(to_serialize, fields=fields, request=request)

    def serialize_instance(self, instance) -> dict:

        price = sum(game.price for game in instance.games.all())
        return {
            'id': instance.pk,
            'status': instance.get_status_display(),
            'created_at': instance.created_at,
            'updated_at': instance.updated_at,
            'key': None,
            'games':[
                {
                    'id': game.pk,
                    'title': game.title,
                    'slug': game.slug,
                    'description': game.description,
                    'cover': self.build_url(game.cover.url),
                    'price': game.price,
                    'stock': game.stock,
                    'released_at': game.released_at,
                    'pegi': game.get_pegi_display(),
                    'category': {
                        'id': game.category.pk,
                        'name': game.category.name,
                        'slug': game.category.slug,
                        'description': game.category.description,
                        'color': game.category.color,
                    },
                    'platforms':[
                        {
                            'id': platform.pk,
                            'name': platform.name,
                            'slug': platform.slug,
                            'description': platform.description,
                            'logo': self.build_url(platform.logo.url),
                        }
                        for platform in game.platforms.all()
                    ]
                }
                for game in instance.games.all()
            ],
            
            'author':{
                'id': instance.user.id,
                'username': instance.user.username,
                'email': instance.user.email,
                'first_name': instance.user.first_name,
                'last_name': instance.user.last_name,
            },
            'price': price
        }
