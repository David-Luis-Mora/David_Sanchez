from shared.serializers import BaseSerializer
from games.serializers.games_serializers import GamesSerializer
from users.serializers.users_serializers import UserSerializer
class OrdersSerializer(BaseSerializer):
    def __init__(self, to_serialize, *, fields=[], request=None):
        super().__init__(to_serialize, fields=fields, request=request)

    def serialize_instance(self, instance) -> dict:

        price = sum(game.price for game in instance.games.all())
        return {
            'id': instance.pk,
            'status': instance.get_status_display(),
            'created_at': instance.created_at.isoformat(),
            'updated_at': instance.updated_at.isoformat(),
            'key': None,
            'games': GamesSerializer(instance.games.all(), request=self.request).serialize(),
            'user': UserSerializer(instance.user).serialize(),
            'price': price
        }
